<template>
    <div class="tab-container">
        <el-form :model="form" ref="formRef" :rules="validationRules" label-width="120px">
            <template v-for="(field, index) in schema.fields" :key="field.model">
                <!-- <el-row><el-col :span="12"> -->
                <div :class="['form-group', field.layout || 'vertical']">
                    <el-form-item 
                        :prop="field.model" 
                        v-show="!field.hidden && visibleFields[field.model]"
                    >
                        <template #label>
                            {{ field.label }}
                            <el-popover
                                v-if="field.tooltip"
                                placement="bottom"
                                trigger="hover"
                                width="200"
                                :content="field.tooltip"
                            >
                                <template #reference>
                                    <el-icon class="tooltip-icon">
                                        <QuestionFilled />
                                    </el-icon>
                                </template>
                            </el-popover>
                        </template>

                        <component
                            :is="getFieldComponent(field)"
                            v-bind="getFieldProps(field)"
                            v-model="form[field.model]"
                        >
                            <!-- Render options for select, radio, and checkbox -->
                            <el-option
                                v-if="field.type === 'select'"
                                v-for="option in field.options"
                                :key="option.value"
                                :label="option.label"
                                :value="option.value"
                            />
                            <el-radio
                                v-if="field.type === 'radio'"
                                v-for="option in field.options"
                                :key="option.value"
                                :label="option.value"
                            >
                                {{ option.label }}
                            </el-radio>
                            <el-checkbox
                                v-if="field.type === 'checkbox'"
                                v-for="option in field.options"
                                :key="option.value"
                                :label="option.value"
                            >
                                {{ option.label }}
                            </el-checkbox>
                        </component>
                    </el-form-item>
                    <div v-if="field.comments" class="form-comments">{{ field.comments }}</div>
                </div>
                <!-- </el-col></el-row> -->
            </template>
            <el-form-item>
                <el-button type="primary" @click="onSubmit">Submit</el-button>
                <el-button @click="onCancel">Cancel</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>

  
  
<script>
import { reactive, ref, watch, onMounted } from "vue";
import { ElMessage } from "element-plus";
import EventBus from "@/utils/eventBus";
import useStore from "@/store";
import { apiRequest } from "@/api/table";
import { QuestionFilled } from "@element-plus/icons-vue";

export default {
    name: "FormTemplate",
    props: {
        formdata: {
            type: Object,
            default: () => ({}),
        },
        formtype: {
            type: String,
            required: true
        },
        schema: {
            type: Object,
            required: true
        }
    },
    components: {
        QuestionFilled
    },
    setup(props) {
        const formRef = ref(null);
        const form = reactive({});
        const validationRules = reactive({});
        const columnNameMap = reactive(new Map())
        const visibleFields = reactive({});

        const resetFieldValue = (field) => {
            // Reset to default value if defined, or to an empty state otherwise
            if (field.type === "checkbox") {
                form[field.model] = [];
            } else if (field.type === "select" && field.options) {
                const defaultOption = field.options.find((option) => option.default);
                form[field.model] = defaultOption ? defaultOption.value : "";
            } else {
                form[field.model] = ""; // Default to empty string for other field types
            }
        };

        const computeVisibility = () => {
            props.schema.fields.forEach((field) => {
                if (field.visibility) {
                    const { dependsOn, condition } = field.visibility;

                    // Collect values of all dependent fields
                    const dependencyValues = {};
                    dependsOn.forEach((dep) => {
                        dependencyValues[`${dep}Value`] = form[dep];
                    });

                    // Dynamically evaluate the condition with the dependent values
                    try {
                        const isVisible = new Function(
                            ...Object.keys(dependencyValues),
                            `return ${condition}`
                        )(...Object.values(dependencyValues));

                        // Update visibility
                        visibleFields[field.model] = isVisible;

                        // Reset the field value if it becomes hidden
                        if (!isVisible) {
                            resetFieldValue(field);
                        }
                    } catch (error) {
                        console.error(`Error evaluating visibility condition for ${field.model}:`, error);
                        visibleFields[field.model] = true; // Default to visible in case of error
                    }
                } else {
                    visibleFields[field.model] = true; // Default to visible if no condition is specified
                }
            });
        };

        const getValidationRule = (rule, field) => {
            if (rule === "required") {
                return { required: true, message: `${field.label} is required`, trigger: "blur" };
            }
            if (rule === "email") {
                return {
                    type: "email",
                    message: "Please enter a valid email",
                    trigger: "blur",
                };
            }
            // Add more validation rules as needed
        };

        const getFieldComponent = (field) => {
            let comp = "el-input";
            switch(field.type) {
                case "text":
                    comp = "el-input";
                    break;
                case "select":
                    comp = "el-select";
                    break;
                case "radio":
                    comp = "el-radio-group";
                    break;
                case "checkbox":
                    comp = "el-checkbox-group";
                    break;
            };
            //console.log("field = ", field.model, " | component = ", comp);
            return comp;
        };

        const getFieldProps = (field) => {
            const props = { placeholder: field.placeholder || "" };
            if (field.type === "select" || field.type === "radio" || field.type === "checkbox") {
                props.options = field.options;
            }
            //console.log("field.model = ", field.model, " | props = ", props);
            return props;
        };

        const getFieldRules = (field) => {
            let rule = validationRules[field.model] || [];
            console.log("field.model = ", field.model, " | rule = ", rule);
            return rule
        };

        const getFormName = () => {
            const { formName } = props.schema;
            return 
        };

        const initializeForm = () => {
            props.schema.fields.forEach((field) => {
                if (field.type === "checkbox") {
                    form[field.model] = [];
                } else if(field.type === "select") {
                    console.log("select type: ", field.model)
                    form[field.model] = "";
                    field.options.forEach(opt => {
                        console.log(opt)
                        if (opt.hasOwnProperty("default") && opt.default ) {
                            console.log("default value", opt.value)
                            form[field.model] = opt.value;
                        }
                    });
                } else {
                    form[field.model] = "";
                };
                //form[field.model] = field.type === "checkbox" ? [] : ""; // Initialize checkbox with an empty array
                
                if (field.rules && field.rules.length > 0) {
                    validationRules[field.model] = field.rules.map((rule) =>
                        getValidationRule(rule, field)
                    );
                }
                columnNameMap.set(field.column, field.model);
            });

            // initialize for edit mode
            if (props.formtype === "edit") {
                if (props.formdata && Object.keys(props.formdata).length > 0) {
                    console.log("Populating form with newData..."); // Debug: Log action
                    Object.keys(props.formdata).forEach((key) => {
                        let lkey = columnNameMap.get(key);
                        if (lkey in form) {
                            form[lkey] = props.formdata[key];
                        }
                    });
                    console.log("initialized for edit mode");
                }
            };
            
            computeVisibility();
            console.log("form value = ", form);
        };

        // Reset the form to blank values
        const resetForm = () => {
            Object.keys(form).forEach((key) => {
                form[key] = Array.isArray(form[key]) ? [] : "";
            });
        };

        const user = useStore().user;

        const onSubmit = async () => {
            console.log("data to be submitted:", form);
            
            try {
                //const { addFunction, editFunction } = props.schema;

                let payload = { ...form };
                payload.mail = user.info.mail;
                console.log("payload = ", payload)

                let response = undefined;
                if (props.formtype === "edit") {
                    response = await apiRequest(props.schema.functions.edit, payload);
                } else {
                    response = await apiRequest(props.schema.functions.add, payload);
                }
                console.log("API response: ", response);

                ElMessage.success(
                    form.gid ? "Record updated successfully!" : "Record created successfully!"
                );

                EventBus.emit("passfunction", {
                    options: "list",
                    comName: "ListTemplate",
                });
                EventBus.emit("refreshGradeTable", {});
            } catch (error) {
                console.log("API failed: ", error);
                ElMessage.error(
                    form.gid ? "Record updated failed!" : "Record created failed!"
                );
            }

        };

        watch(() => form, 
            computeVisibility, 
            { deep: true }
        ); // Recompute visibility on data change

        const onCancel = () => {
            resetForm(); // Reset form on cancel
            const params = {
                options: "list",
                comName: "ListTemplate",
            };
            EventBus.emit("passfunction", params);
        };

        onMounted(() => {
            console.log("Component mounted, form initialized");
            initializeForm();
        });

        return {
            form,
            columnNameMap,
            formRef,
            onSubmit,
            onCancel,
            getFieldProps,
            getFieldRules,
            getFormName,
            getValidationRule,
            getFieldComponent,
            validationRules,
            visibleFields,
            QuestionFilled
        };
    },
};
</script>
  
  
  
<style scoped>
.tab-container {
    margin: 30px;
}
.tooltip-icon {
    cursor: pointer;
    color:blue;
}
.tab-container .form-group {
    display: flex;
    flex-wrap: wrap; /* Allows wrapping if needed */
    gap: 16px; /* Space between fields */
    align-items: flex-start;
    width: auto;
}

.tab-container .form-group.horizontal {
    flex-direction: row;
    justify-content: flex-start;
}

.tab-container .form-group.vertical {
    flex-direction: column;
    width: 100%;
}

.tab-container .el-input,
.tab-container .el-select,
.tab-container .el-radio-group,
.tab-container .el-checkbox-group {
    /* max-width: 300px; Set a max width */
    /* min-width: 150px; */
    flex: 1; /* Allow responsive scaling */
    width: 300px; /* Full width within the container */
}
</style>
  