<script setup lang="ts">
import { reactive, ref, watch, onMounted, computed, nextTick  } from "vue";
import { ElMessage, ElMessageBox  } from "element-plus";
import EventBus from "@/utils/eventBus";
import useStore from "@/store";
import { apiRequest } from "@/api/table";
import { QuestionFilled } from "@element-plus/icons-vue";
import MultiInputs from "./MultiInputs.vue";

// Props
const props = defineProps({
    formData: {
        type: Object,
        default: () => ({}),
    },
    formType: {
        type: String,
        required: true
    },
    schema: {
        type: Object,
        required: true
    }
});

// State
const formRef = ref(props.schema.formName);
const form = reactive({});
const validationRules = reactive({});
const visibleFields = reactive({});
const visibleComments = reactive({});
const formLoading = ref(true);
const dataStore = reactive({}); //for preload data
const typeStore = reactive({}); //for reload data type
const formType = ref("")
const assignee = reactive({})
const customerModalVisible = ref(false);
const stopSignal = reactive({});
const teleported = ref(false);
const formDisabled = ref(false);
const disabledFields = reactive({});
const preDisabledFields = reactive({});
const disabledMultiInputs = reactive({});
const caculatedFieldOptionNumber = reactive({});
const newCustomerForm = reactive({
    field_jira_id: '',
    field_customer_name: '',
    field_customer_id: '',
    field_description: '',
    field_customer_olcs: '',
    field_customer_impact: '',
    field_ont_plm: '',
    field_nwf_plm: '',
    field_fwa_plm: '',
    field_local_contact: '',
})
// Store
const user = useStore().user;
const mail = user.getUser().mail;

const headerFields = () => {
    const fields = props.schema.fields.filter((field) => field.header === true)
    //console.log("headerFields = ", fields)
    return fields
}
const normalFields = () => {
    const fields = props.schema.fields.filter((field) => !field.header)
    //console.log("normalFields = ", fields)
    return fields
}

const preloadData = async () => {
    if (!props.schema.preload) {
        formLoading.value = false;
        return
    }
    try {
        const payload = { type: "all", mail: mail };
        formLoading.value = true;

        // Create an array of promises for all preload operations
        const preloadPromises = Object.entries(props.schema.preload).map(async ([key, { api, type, mapKey }]) => {
            //const ttype = props.schema.preload[key].type;
            const response = await apiRequest(api, payload);
            typeStore[key] = type;

            if (type === "array") {
                dataStore[key] = response.data.items;
            } else if (type === "map") {
                // Transform the array into a hash map
                dataStore[key] = response.data.items.reduce((map, item) => {
                    const keyValue = item[mapKey];
                    if (keyValue) {
                        map[keyValue] = item;
                    }
                    return map;
                }, {});
            }
        });
        // Wait for all promises to complete
        await Promise.all(preloadPromises);
    } catch (error) {
        console.error("Error preloading data:", error);
    } finally {
        formLoading.value = false;
    }
};

// const handleStopSignal = () => {
//     Object.keys(visibleFields).forEach(key => {
//         if (visibleFields[key]) {
            
//         } 
//     });
// }

// Populate dependent fields
const populateDependentFields = (field) => {
    //console.log("populateDependentFields, ", field.model)
    field.dependsOn.forEach((dependency) => {
        const dependencyValue = form[dependency.field];
        if (dependency.from) {
            const sourceData = dataStore[dependency.from.source];
            const mappedValue = sourceData.find(
                (item) => item[dependency.from.attribute] === dependencyValue)?.[dependency.from.key];
            form[field.model] = mappedValue || "";
        }

        if (dependency.by) {
            const dependencyValue = form[dependency.field];
            const conditionalValue = form[dependency.conditionalField];
            const sourceData = dataStore[dependency.by.source];
            const conditionalKeys = dependency.by.conditionalKeys || {};
            console.log("conditionalKeys[conditionalValue] = ", conditionalKeys[conditionalValue])
            const keyToUse = conditionalKeys[conditionalValue].field;
            console.log("keyToUse = ", keyToUse)
            console.log("dependencyValue = ", dependencyValue)
            console.log("conditionalValue = ", conditionalValue)
            console.log("conditionalKeys = ", conditionalKeys)
            //console.log("sourceData = ", sourceData)
            let mappedValue = "";
            if (keyToUse) {
                mappedValue = sourceData.find(
                (item) => item[dependency.by.attribute] === dependencyValue)?.[keyToUse];
            }
            console.log("mappedValue = ", mappedValue)
            form[field.model] = mappedValue || conditionalKeys[conditionalValue].default || "";
            const key = `${dependencyValue}-${conditionalValue}`
            if (Object.keys(assignee).includes(key)) {
                form[field.model] = assignee[key]
            }
        }

        if (dependency.filter && dependency.mapToOption) {
            const sourceData = dependency.filter.mapFrom
            //console.log("sourceData", dataStore[sourceData])
            const filteredOptions = dataStore[sourceData].filter(
                (item) => item[dependency.filter.attribute] === dependencyValue
            );
            //console.log("filteredOptions", filteredOptions)
            const uniqueOptions = new Set();
            const fieldOptions = filteredOptions.map((item) => {
                const val = dependency.mapToOption.replace(
                    /\{(\w+)\}/g,
                    (_, key) => item[key] || ""
                );
                return {label: val, value: val}
            }).filter((option) => {
                const key = `${option.label}-${option.value}`;
                if (uniqueOptions.has(key)) {
                    return false;
                }
                uniqueOptions.add(key);
                return true;
            });
            //console.log("fieldOptions = ", fieldOptions);
            field.options = fieldOptions;
            // if (field.stopMessage ) {
            //     if (visibleFields[field.model] && fieldOptions.length === 0) {
            //         ElMessageBox.alert(field.stopMessage, 'Attention!', {
            //             confirmButtonText: 'OK',
            //         })
            //     } else {
            //         stopSignal[field.model] = (fieldOptions.length <= 0) ? true: false;
            //     }
            // }
            caculatedFieldOptionNumber[field.model] = fieldOptions.length
            console.log(`put caculatedFieldOptionNumber[${field.model}] = ${fieldOptions.length}`)
            form[field.model] = ""
        }
    });
};
// Populate dependent fields
const populateValueFrom = (field) => {
    field.valuefrom.forEach((dependency) => {
        console.log("populateValueFrom")
        const dependencyValue = form[dependency.field];
        const conditionalValue = form[dependency.conditionField];
        if (dependency.from) {
            const sourceData = dataStore[dependency.from.source];
            const conditionalKeys = dependency.from.conditionalKeys || {};
            const keyToUse = conditionalKeys[conditionalValue] || 
                dependency.from.defaultKey;
            const mappedValue = sourceData.find(
                (item) => item[dependency.from.attribute] === dependencyValue)?.[keyToUse];
            form[field.model] = mappedValue || "";
        }
    });
};

// Functions
const resetFieldValue = (field) => {
    if (field.type === "checkbox") {
        form[field.model] = [];
    } else if (field.type === "select" && field.options) {
        const defaultOption = field.options.find((option) => option.default);
        form[field.model] = defaultOption ? defaultOption.value : "";
    } else {
        form[field.model] = "";
    }
};

const fieldVisibility = (field) => {
    if (field.visibility) {
        const { dependsOn, condition } = field.visibility;
        const dependencyValues = Object.fromEntries(dependsOn.map(dep => [`${dep}Value`, form[dep]]));
        try {
            const isVisible = new Function(...Object.keys(dependencyValues), `return ${condition}`)(...Object.values(dependencyValues));
            visibleFields[field.model] = isVisible;
            if (isVisible) {
                validationRules[field.model] = field.rules.map((rule) => getValidationRule(rule, field));
                // if (field.stopMessage && stopSignal[field.model]) {
                //     ElMessageBox.alert(field.stopMessage, 'Attention!', {
                //         confirmButtonText: 'OK',
                //     })
                // }
                //console.log("validationRule = ", validationRules[field.model]);
            } else {
                resetFieldValue(field);
                //validationRules[field.model] = {};
                if (field.type === "checkbox") {
                    validationRules[field.model] = { type: "array", required: false, trigger: "submit"};
                } else {
                    validationRules[field.model] = {};
                }
            }
        } catch (error) {
            console.error(`Error evaluating visibility for ${field.model}:`, error);
            visibleFields[field.model] = true;
        }  
    } else {
         visibleFields[field.model] = true;
         validationRules[field.model] = field.rules.map((rule) => getValidationRule(rule, field));
    }
};

const commentVisibility = (field) => {
    if (field.comments) {
        if (field.commentVisibility) {
            const { dependsOn, condition } = field.commentVisibility;
            const dependencyValues = Object.fromEntries(dependsOn.map(dep => [`${dep}Value`, form[dep]]));
            console.log(`${field.model}.dependsOn = `, dependsOn)
            console.log(`${field.model}.condition = `, condition)
            console.log(`${field.model}.dependencyValues = `, dependencyValues)
            try {
                const isVisible = new Function(...Object.keys(dependencyValues), `return ${condition}`)(...Object.values(dependencyValues));
                visibleComments[field.model] = isVisible;
                console.log(`${field.model}.comments.visibility = ${isVisible}`);
            } catch (error) {
                console.log(`Error evaluating visibility for comment ${field.model}:`, error);
                visibleComments[field.model] = true;
            }
        } else {
            visibleComments[field.model] = true;
        }
    };
}

const computeVisibility = () => {
    props.schema.fields.forEach((field) => {
        field.model && fieldVisibility(field);
        nextTick(() => {
            field.model && commentVisibility(field);
        });
    });
};

const isValidOption = (option) => {
    if(!option.valid) {
        return true;
    }

    try {
        const {field, condition} = option.valid;
        const targetValues = Object.fromEntries(field.map(dep => [`${dep}Value`, form[dep]]));
        const isValid = new Function(...Object.keys(targetValues), `return ${condition}`)(
            ...Object.values(targetValues)
        );
        return isValid;
    } catch(error) {
        console.error("Error evaluating condition:", option, error);
        return false;
    }
}

const getValidationRule = (rule, field) => {
    switch (rule) {
        case "required":
            if (field.type === "checkbox") {
               return { type: "array", required: true, message: "Please select at least one option." , trigger: "submit"}
            } else {
                return { required: true, message: `${field.label} is required`, trigger: "submit" };
            }
        case "email":
            return { type: "email", message: "Please enter a valid email", trigger: "submit" };
        default:
            return {};
    }
};

const getFieldComponent = (field) => {
    return {
        text: "el-input",
        select: "el-select",
        radio: "el-radio-group",
        checkbox: "el-checkbox-group",
        textarea: "el-input",
        file: "el-upload",
        date: "el-date-picker",
    }[field.type] || "el-input";
};

const getFieldProps = (field) => {
    const props = { placeholder: field.placeholder || "" };
    //const props = {};

    switch (field.type) {
        case "textarea":
            props.type = field.type
            break;
        case "file":
            props.action = "api/common/upload"
            props.accept = field.accept || "*/*" //Allowed file types
            props.showFileList = false //Hide the default file list
            props.onSuccess = (response, file) => handleFileSuccess(file, field, response);
            props.beforeUpload = handleBeforeUpload
            break;
        case "select":
            props.filterable = true;
            break;
        case "date":
            props.type = 'date'
            props.teleported = false
            props['validate-event'] = false
            //console.log(`field = ${field.model}, props = `, props)
    }

    if (field.disabled) {
        props.disabled = true;
        preDisabledFields[field.model] = true;
        disabledFields[field.model] = true;
        console.log(`${field.model} disabled = ${field.disabled}`);
    }
    
    //console.log(`field = ${field.model}, props = `, props);
    return props;
};

const populateFieldOptions = (field) => {
    if (field.optionSource) {
        //console.log("typeStore[field.optionSource.data] = ", typeStore[field.optionSource.data])
        switch (typeStore[field.optionSource.data]) {
            case "array":
                // Check if a condition exists in optionSource
                const conditionFn = field.optionSource.condition
                    ? new Function("value", `return ${field.optionSource.condition}`)
                    : () => true; // Default condition to include all values

                field.options = Array.from(
                    new Set(
                        dataStore[field.optionSource.data]
                            .map((item) => item[field.optionSource.field])
                            .filter((value) =>
                                value !== undefined && 
                                value !== null &&
                                conditionFn(value)
                            ) // Filter out undefined/null values
                    )
                )
                .sort((a, b) => {
                    // Customize the sort order if needed (default is ascending)
                    if (typeof a === "string" && typeof b === "string") {
                        return a.localeCompare(b); // String comparison
                    }
                    return a > b ? 1 : -1; // Numeric or default comparison
                })
                .map((value) => ({
                    label: value,
                    value: value,
                }));
                break;
            case "map":
                break;
        }
        if (props.formType === "edit" && Object.keys(props.formData).length > 0) {
            form[field.model] = props.formData[field.model]
        }
    } 
}

const initializeForm = () => {
    props.schema.fields.forEach((field) => {
        //field.model && resetFieldValue(field);
        if (field.model) {
            if (field.type === 'group') {
                field.fields.forEach(f => {
                    resetFieldValue(f)
                });
            } else {
                resetFieldValue(field);
            }
            //console.log(`field.model = ${field.model}, field.value = ${form[field.model]}`)
        }
        populateFieldOptions(field);
        if (Object.keys(props.formData).length > 0) {
            if (props.formType === 'edit') {
                Promise.resolve().then(() => {
                    //props.schema.fields.forEach(field => {
                    if (field.model) {
                        const val = props.formData[field.model]
                        if ( field.type === "checkbox") {
                            if (val) {
                                if (val.includes(';;;')) {
                                    form[field.model] = val.split(";;;");
                                } else {
                                    form[field.model] = val.split(";");
                                }
                            } else {
                                form[field.model] = []
                            }
                            //form[field.model] = val ? val.split(";;;") : []
                            console.log(`form.${field.model} = ${form[field.model]}`)
                        }else if (field.type === "group") {
                            field.fields.forEach(f => {
                                form[f.model] = props.formData[f.model]
                            });
                        } else {
                            form[field.model] = val
                        };
                    }
                });
            } else {
                Promise.resolve().then(() => {
                    const l_array = ['field_customer', 'field_managed_by_hc']
                    if (l_array.includes(field.model)) {
                        form[field.model] = props.formData[field.model];
                    }
                });
            }
        }
    });

    computeVisibility();
    // Promise.resolve().then(() => {
    //     if (Object.keys(form).includes('field_status')) {
    //         onStatusChange();
    //     }
    // });

    console.log("form = ", form)
};

const resetForm = () => {
    Object.keys(form).forEach((key) => {
        form[key] = Array.isArray(form[key]) ? [] : "";
    });
};

const get_ts = () => {
    const d = new Date();
    let ret = d.getFullYear() + '-' +
        (d.getMonth() + 1).toString().padStart(2, '0') + '-' +
        d.getDate().toString().padStart(2, '0') + ' ' +
        d.getHours().toString().padStart(2, '0') + ':' +
        d.getMinutes().toString().padStart(2, '0') + ':' +
        d.getSeconds().toString().padStart(2, '0')

    return ret
}

const onSubmit = async () => {
    try {
        console.log("form data = ", form)
        await formRef.value.validate();
        let data = {}
        console.log("formType == ", props.formType)
        Object.keys(form).forEach(key => {
            if (Array.isArray(form[key])) {
                data[key] = form[key].join(';;;')
            } else {
                data[key] = form[key] || ''
            }
        });
        if (props.formType === 'edit') {
            data = {
                ...data,
                modifier: mail,
                modifiedon: get_ts()
            }
        } else {
            data = {
                ...data,
                creator: mail,
                createon: get_ts()
            }
        }
        console.log("data = ", data)
        const payload = { ...data, mail: mail };
        const response = await apiRequest(props.schema.functions[props.formType], payload);
        ElMessage.success(props.formType === "edit" ? "Record updated successfully!" : "Record created successfully!");
        EventBus.emit(props.schema.notifications.switch, { options: "list", comName: "ListTemplate" });
        EventBus.emit(props.schema.notifications.refresh, {});
    } catch (error) {
        console.error("submit failed:", error);
        ElMessage.error(props.formType === "edit" ? "Record update failed!" : "Record creation failed!");
    }
};

function getListeners(field) {
    const listener = {}
    if (field.onInput && typeof this[field.onInput] === 'function') {
        // const listener = {}
        listener.input = this[field.onInput]
    }
    if (field.change && typeof this[field.change.func] === 'function') {
        // const listener = {}
        listener.change = (event, f) => {
            this[field.change.func](event, field)
        }
    }
    return listener    
}
function getButtonClass(field) {
    if (field.class) {
        return field.class || '';
    }
}
function handleButtonClick(field) {
    if (field.onClick && typeof this[field.onClick] === 'function') {
        this[field.onClick]();
    } else {
        console.error('No valid handler found for this button!')
    }
}


function onAssigneeInput (value){
    console.log("onAssigneeInput, value = ", value)
    // const customer = form.field_customer
    // const status = form.field_status
    const key = `${form.field_customer}-${form.field_status}`
    console.log("onAssigneeInput, key = ", key)
    assignee[key] = value
}

//
// for new customer add
//
function onCustomerAddClick() {
    //onsole.log("onCustomerAddClick")
    customerModalVisible.value = true;
    console.log("customerModalVisible = ", customerModalVisible.value)
}
async function onCustomerModalAddClick() {
    //onsole.log("onCustomerAddClick")

    try {
        const payload = { ...newCustomerForm, mail: mail };
        const response = await apiRequest("customerAdd", payload);
        if (response.code === 20000) {
            dataStore.customerData.push({
                customer: newCustomerForm.field_customer_name,
                key: newCustomerForm.field_jira_id,
                cid: newCustomerForm.field_customer_id
            });
            const field = props.schema.fields.filter((field) => field.model === 'field_customer')[0];
            populateFieldOptions(field);
            if (Object.keys(form).includes('field_customer')) {
                form.field_customer = newCustomerForm.field_customer_name;
            }
            customerModalVisible.value = false;
            console.log("customerModalVisible = ", customerModalVisible.value)
            customerReset();
        } else {
            console.error("customer add failed, code:", response.code);
            ElMessage.error("customer add failed, code: ", response.code);
        }
    } catch (error) {
        console.error("customer add failed:", error);
        ElMessage.error("customer add failed: ", error);
    }
}
function onCustomerModalCancelClick() {
    //onsole.log("onCustomerAddClick")
    customerModalVisible.value = false;
    console.log("customerModalVisible = ", customerModalVisible.value)
    customerReset();
}
function customerReset() {
    Object.keys(newCustomerForm).forEach(key => {
        newCustomerForm[key] = ''
    });
}
async function onAddDeviceDPClick() {
    try {
        console.log("form data = ", form)
        await formRef.value.validate();
        let data = {}
        console.log("formType == ", props.formType)
        Object.keys(form).forEach(key => {
            if (Array.isArray(form[key])) {
                data[key] = form[key].join(';;;')
            } else {
                data[key] = form[key]
            }
        });
        if (props.formType === 'edit') {
            data = {
                ...data,
                modifier: mail,
                modifiedon: get_ts()
            }
        } else {
            data = {
                ...data,
                creator: mail,
                createon: get_ts()
            }
        }
        console.log("data = ", data)
        const payload = { ...data, mail: mail };
        const response = await apiRequest(props.schema.functions[props.formType], payload);
        ElMessage.success(props.formType === "edit" ? "Record updated successfully!" : "Record created successfully!");
        //console.log(props.schema.functions);
        EventBus.emit(props.schema.notifications.switch, {
            options: "add-device",
            rowData: {
                field_customer: form.field_customer,
                field_managed_by_hc: 'Yes',
            }
        });
    } catch (error) {
        console.error("submit failed:", error);
        ElMessage.error(props.formType === "edit" ? "Record update failed!" : "Record creation failed!");
    }

}

function onHostedByChange(val, field) {
    console.log("val = ", val)
    if (val !== 'Nokia hosted') {
        //formDisabled.value = true;
        Object.keys(visibleFields).forEach(key => {
            if (key !== 'field_hosted_by' && visibleFields[key]) {
                disabledFields[key] = true;
            }
        });
        ElMessageBox(field.change.message)
    } else {
        //formDisabled.value = false;
        Object.keys(visibleFields).forEach(key => {
            if (visibleFields[key] && !Object.keys(preDisabledFields).includes(key)) {
                disabledFields[key] = false;
            }
        });
    };
}

function onMultiLegalChange(val, field) {
    console.log("val = ", val)
    if (val !== 'Yes') {
        //formDisabled.value = true;
        Object.keys(visibleFields).forEach(key => {
            if (key !== 'field_multi_legal_clearance' && visibleFields[key]) {
                disabledFields[key] = true;
            }
        });
        ElMessageBox(field.change.message)
    } else {
        //formDisabled.value = false;
        Object.keys(visibleFields).forEach(key => {
            if (visibleFields[key] && !Object.keys(preDisabledFields).includes(key)) {
                disabledFields[key] = false;
            }
        });
    };
}

function onDedicatedLegalChange(val, field) {
    console.log("val = ", val)
    if (val !== 'Yes') {
        //formDisabled.value = true;
        Object.keys(visibleFields).forEach(key => {
            if (key !== 'field_dedicated_legal_clearance' && visibleFields[key]) {
                disabledFields[key] = true;
            }
        });
        ElMessageBox(field.change.message)
    } else {
        //formDisabled.value = false;
        Object.keys(visibleFields).forEach(key => {
            if (visibleFields[key] && !Object.keys(preDisabledFields).includes(key)) {
                disabledFields[key] = false;
            }
        });
    };
}

function onRootDeviceOptionsUpdate(val, field) {
    console.log("val = ", val, ", field = ", field.model)
    const target_field = "field_home_controller"
    const target_field_2 = "field_managed_by_hc"
    console.log(`access caculatedFieldOptionNumber[${target_field}] =  ${caculatedFieldOptionNumber[target_field]}`)
    if (Object.keys(visibleFields).includes(target_field) && 
        caculatedFieldOptionNumber[target_field] === 0 &&
        form[target_field_2] === "Yes"
    ) {
        Object.keys(visibleFields).forEach(key => {
            if (key !== field.model && visibleFields[key]) {
                disabledFields[key] = true;
            }
        });
        ElMessageBox(field.change.message)
    } else {
        Object.keys(visibleFields).forEach(key => {
            if (visibleFields[key] && !Object.keys(preDisabledFields).includes(key)) {
                disabledFields[key] = false;
            }
        });
    }
}

function onStatusChange(val, field) {
    if (!val) {
        return;
    }
    console.log("val = ", val)
    const exceptionFields = [
        'field_status',
        'field_assignee',
        'field_ouid',
        'field_additional'
    ]
    const groupItems = props.schema.fields.filter((f) => f.type === 'group');
    const groupKeys = groupItems.map(obj => (obj.model))
    console.log(`groupKeys = ${groupKeys}`)
    if (val !== 'New') {
        //formDisabled.value = true;
        Object.keys(visibleFields).forEach(key => {
            if (!exceptionFields.includes(key) && visibleFields[key]) {
                if (groupKeys.includes(key)) {
                    groupItems.filter((k) => k.model === key)[0].fields.forEach(f => {
                        disabledMultiInputs[f.model] = true;
                    });
                } else {
                    disabledFields[key] = true;
                }
            }
        });
        //ElMessageBox(field.change.message)
    } else {
        //formDisabled.value = false;
        Object.keys(visibleFields).forEach(key => {
            if (!exceptionFields.includes(key) && !Object.keys(preDisabledFields).includes(key)) {
                if (groupKeys.includes(key)) {
                    groupItems.filter((k) => k.model === key)[0].fields.forEach(f => {
                        disabledMultiInputs[f.model] = false;
                    });
                } else {
                    disabledFields[key] = false;
                }
            }
        });
    };
}

const caculateLabelSpan = (field) => {
    switch (field.span) {
        case 8:
        case 12:
            return 8;
        case 24:
            return 4;

    }
}
const caculateFieldSpan = (field) => {
    if (field.type === "textarea") {
        return 20;
    } else {
        switch (field.span) {
            case 8:
            case 12:
                return 16;
            case 24:
                if (field.model === 'field_customer_id') {
                    return 20;
                } else {
                    return 8;
                };
                
        }
    }
}

// Handle file upload success
function handleFileSuccess(file, field, response) {
    // const fileURL = URL.createObjectURL(file.raw); // Generate temporary file URL
    // form[field.model] = {
    //     name: file.name,
    //     url: fileURL,
    // };
    console.log(`response = ${response}`)
    //const fileURL = 'api/common/download?file=' + response.data.name;
    form[field.model] = response.data.name;
}
function generateDownloadLink(field) {
    return 'api/common/download?file=' + form[field.model];
}
// Validate file size before upload
function handleBeforeUpload(file) {
    const isLt5M = file.size / 1024 / 1024 < 5;
    if (!isLt5M) {
        ElMessage.error("File size must be less than 5MB!");
        return false;
    }
    return true;
}

const onCancel = () => {
    resetForm();
    EventBus.emit(props.schema.notifications.switch, { options: "list", comName: "ListTemplate" });
};


// Watchers
//watch(() => form, computeVisibility, { deep: true });
// Watch for changes in dependent fields
props.schema.fields.forEach((field) => {
  if (field.dependsOn && field.dependsOn.length > 0) {
    watch(() => form[field.dependsOn[0]?.field], () => populateDependentFields(field));
    if (field.dependsOn[0].conditionalField) {
        watch(() => form[field.dependsOn[0]?.conditionalField], () => populateDependentFields(field));
    }
  }
  //if (field.valuefrom && field.valuefrom.length > 0) {
  //  watch(() => form[field.valuefrom[0]?.field], () => populateValueFrom(field));
  //}
  if (field.visibility) {
    field.visibility.dependsOn.forEach(dep => {
        watch(() => form[dep], () => fieldVisibility(field));
    });
  }

  if (field.commentVisibility) {
    field.commentVisibility.dependsOn.forEach(dep => {
        watch(() => form[dep], () => commentVisibility(field));
    });
  }
});

// Lifecycle
onMounted(async () => {
    await preloadData();
    initializeForm();
    formType.value = props.formType
    console.log("formType == ", props.formType)
    nextTick(() => {
        if (Object.keys(form).includes('field_status')) {
            onStatusChange(form.field_status);
        }
    });
});
</script>

<template>
    <div class="tab-container">
        <el-form 
            :model="form" 
            ref="formRef" 
            :rules="validationRules" 
            label-width="0px"
            :validate-on-rule-change="false"
            v-loading="formLoading"
            :disabled="formDisabled"
        >
            <el-card 
                v-if="headerFields().length > 0"
                class="form-header" 
                body-style="padding: 5px 0px 0px 0px;"
            >
                <el-row :gutter="20">
                    <template v-for="(field, index) in headerFields()" :key="field.model">
                        <el-col :span="field.size.item">
                            <el-row>
                                <el-col :span="field.size.label">
                                    <div class="form-label">
                                        {{ field.label }}
                                    </div>
                                </el-col>
                                <el-col :span="field.size.field">
                                    <el-form-item 
                                        :prop="field.model" 
                                        v-show="!field.hidden && visibleFields[field.model]">
                                        <component
                                            :is="getFieldComponent(field)"
                                            v-bind="getFieldProps(field)"
                                            v-model="form[field.model]"
                                            v-on="getListeners(field)"
                                        >
                                            <template v-if="field.type === 'select'">
                                                <template v-for="option in field.options" :key="option.value">
                                                    <el-option
                                                        :label="option.label"
                                                        :value="option.value" />
                                                </template>
                                            </template>
                                        </component>
                                     </el-form-item>
                                </el-col>
                            </el-row>
                        </el-col>
                    </template>
                </el-row>
            </el-card>
            <el-card v-if="normalFields().length > 0" class="form-body">
                <el-row>
                    <template v-for="(field, index) in normalFields()" :key="field.model">
                        <el-col 
                            v-if="field.type === 'button'" 
                            :span="field.size.item" 
                            v-show="!field.hidden"
                        >
                            <el-button type="primary" :class="getButtonClass(field)" @click="handleButtonClick(field)">
                                {{ field.label }}
                            </el-button>
                        </el-col>
                        <el-col v-else :span="field.size.item" v-show="!field.hidden && visibleFields[field.model]">
                            <el-row>
                                <!-- Label Column -->
                                <el-col :span="field.size.label">
                                    <div class="form-label">
                                        {{ field.label }}
                                        <el-popover
                                            v-if="field.tooltip"
                                            placement="bottom"
                                            trigger="hover"
                                            width="200"
                                            :content="field.tooltip">
                                            <template #reference>
                                                <el-icon class="tooltip-icon">
                                                    <QuestionFilled />
                                                </el-icon>
                                            </template>
                                        </el-popover>
                                    </div>
                                </el-col>

                                <!-- Input/Select Column -->
                                <el-col :span="field.size.field">
                                    <el-form-item 
                                        :prop="field.model" 
                                        v-show="!field.hidden && visibleFields[field.model]">
                                        
                                        <!-- File Upload Support -->
                                        <template v-if="field.type === 'file'">
                                            <el-upload
                                                :action="getFieldProps(field).action"
                                                :accept="getFieldProps(field).accept"
                                                :show-file-list="false"
                                                :before-upload="getFieldProps(field).beforeUpload"
                                                :on-success="(response, file) => handleFileSuccess(file, field, response)"
                                            >
                                                <el-button type="primary">Upload File</el-button>
                                            </el-upload>

                                            <!-- File Download Link -->
                                            <div v-if="form[field.model]">
                                                <a 
                                                    :href="generateDownloadLink(field)" 
                                                    target="_blank" 
                                                    download
                                                    style="margin-top: 5px; display: inline-block;"
                                                >
                                                    {{ field.downloadLabel || form[field.model] }}
                                                </a>
                                            </div>
                                        </template>
                                        <template v-else-if="field.type === 'group'">
                                            <MultiInputs
                                                :form="form"
                                                :fields="field.fields"
                                                :disabledFields="disabledMultiInputs"
                                            />
                                        </template>
                                        <template v-else>
                                            <component
                                                :is="getFieldComponent(field)"
                                                v-bind="getFieldProps(field)"
                                                v-model="form[field.model]"
                                                v-on="getListeners(field)"
                                                :disabled="disabledFields[field.model]"
                                            >
                                                <template v-if="['select', 'radio', 'checkbox'].includes(field.type)">
                                                    <template v-if="field.type === 'select'">
                                                        <template v-for="option in field.options" :key="option.value">
                                                            <el-option
                                                                v-if="isValidOption(option)"
                                                                :label="option.label"
                                                                :value="option.value" />
                                                        </template>
                                                    </template>
                                                    <template v-if="field.type === 'radio'">
                                                        <template v-for="option in field.options" :key="option.value">
                                                            <el-radio
                                                            v-if="isValidOption(option)"
                                                            :label="option.value">{{ option.label }}</el-radio>
                                                        </template>
                                                    </template>
                                                    <template v-if="field.type === 'checkbox'">
                                                        <template v-for="option in field.options" :key="option.value">
                                                            <el-checkbox
                                                                v-if="isValidOption(option)"
                                                                :label="option.label"
                                                                :value="option.value" />
                                                        </template>
                                                    </template>
                                                </template>
                                            </component>
                                            <div v-if="field.comments && visibleComments[field.model]" class="form-comments" v-html="field.comments"></div>
                                        </template>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                        </el-col>
                    </template>
                </el-row>
            </el-card>
            <el-card class="form-footer" body-style="padding: 10px 10px 0px 10px; justify-items: center">
                <el-form-item>
                    <el-button type="primary" @click="onSubmit">Submit</el-button>
                    <el-button @click="onCancel">Cancel</el-button>
                </el-form-item>
            </el-card>
        </el-form>


        <el-dialog
    title="Add New Customer"
    v-model="customerModalVisible"
    width="50%">
            <el-form-item label="Jira Key" v-show="false">
                <el-input v-model="newCustomerForm.field_jira_id" />
            </el-form-item>
            <el-form-item label="Description" v-show="false">
                <el-input v-model="newCustomerForm.field_description" />
            </el-form-item>
            <el-form-item label="Customer Name" >
                <el-input v-model="newCustomerForm.field_customer_name" />
            </el-form-item>
            <el-form-item label="Customer Id" >
                <el-input v-model="newCustomerForm.field_customer_id" />
            </el-form-item>
            <el-form-item label="Description" v-show="false">
                <el-input v-model="newCustomerForm.field_description" />
            </el-form-item>
            <el-form-item label="Customer OLCS" v-show="false">
                <el-input v-model="newCustomerForm.field_customer_olcs" />
            </el-form-item>
            <el-form-item label="Customer Impact" v-show="false">
                <el-input v-model="newCustomerForm.field_customer_impact" />
            </el-form-item>
            <el-form-item label="ONT PLM" >
                <el-input v-model="newCustomerForm.field_ont_plm" />
            </el-form-item>
            <el-form-item label="NWF PLM" >
                <el-input v-model="newCustomerForm.field_nwf_plm" />
            </el-form-item>
            <el-form-item label="FWA PLM" >
                <el-input v-model="newCustomerForm.field_fwa_plm" />
            </el-form-item>
            <el-form-item label="Local Contact" >
                <el-input v-model="newCustomerForm.field_local_contact" />
            </el-form-item>
            <template #footer>
                <div class="dialog-footer">
                    <el-button @click="onCustomerModalCancelClick">Cancel</el-button>
                    <el-button type="primary" @click="onCustomerModalAddClick">
                        Add
                    </el-button>
                </div>
            </template>
    </el-dialog>


    </div>

</template>

<style scoped>
.tab-container {
    margin: 30px;
}
.tooltip-icon {
    cursor: pointer;
    color: blue;
}
.tab-container .el-form-item {
    display: flex;
    width: auto;
}
.tab-container .el-col {
    margin-bottom: 2px;

}

.form-comments {
    font-size: smaller;
    color: grey;
}

.form-label {
    padding: 6px 12px;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    font-weight: bold;
    padding-right: 10px;
    /* height: 100%; */
    text-align: right;
}

.tooltip-icon {
    margin-left: 5px;
    cursor: pointer;
}

.el-checkbox-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.form-header {
    margin-bottom: 3px;
    background-color: lightblue;
    .el-form-item {
        margin-bottom: 0px;
    }
    
}

.form-body {
    margin-bottom: 3px;
}

.modal-button {
    width: 150px;
    margin: 2px 0px 0px 30px;
}
</style>
