<script setup lang="ts">
import { reactive, ref, watch, onMounted, computed } from "vue";
import { ElMessage } from "element-plus";
import EventBus from "@/utils/eventBus";
import useStore from "@/store";
import { apiRequest } from "@/api/table";
import { QuestionFilled } from "@element-plus/icons-vue";

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
const formLoading = ref(true);
const formType = ref("")

// Store
const user = useStore().user;
const mail = user.getUser().mail;

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

const getValidationRule = (rule, field) => {
    switch (rule) {
        case "required":
            return { required: true, message: `${field.label} is required`, trigger: "submit" };
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
        textarea: "el-input",
    }[field.type] || "el-input";
};

const getFieldProps = (field) => {
    const props = { placeholder: field.placeholder || "" };

    switch (field.type) {
        case "textarea":
            props.type = field.type
            break;
        case "select":
            props.filterable = true;
            break;
    }
    //console.log(`field = ${field.model}, props = `, props)
    return props;
};

const initializeForm = () => {
    props.schema.fields.forEach((field) => {
        resetFieldValue(field);
        if (props.formType === "edit" && Object.keys(props.formData).length > 0) {
            Promise.resolve().then(() => {
                //props.schema.fields.forEach(field => {
                const val = props.formData[field.model]
                if ( field.type === "checkbox") {
                    form[field.model] = val ? val.split(";;;") : []
                } else {
                    form[field.model] = val
                };
            });
        }
    });
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
        const data = {}
        if (props.formType === 'edit') {
            data.modifier = mail;
            data.modifiedon = get_ts();
        } else {
            data.creator = mail;
            data.createon = get_ts();
        }
        Object.keys(form).forEach(key => {
            if (Array.isArray(form[key])) {
                data[key] = form[key].join(';;;')
            } else {
                data[key] = form[key]
            }
        });
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
                return 8;
        }
    }
}
const onCancel = () => {
    resetForm();
    EventBus.emit(props.schema.notifications.switch, { options: "list", comName: "ListTemplate" });
};

// Lifecycle
onMounted(async () => {
    //await preloadData();
    initializeForm();
    formType.value = props.formType
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
            v-loading="fmLoading"
        >
            <el-card class="form-body">
                <el-row>
                    <template v-for="(field, index) in props.schema.fields" :key="field.model">
                        <el-col :span="field.span" v-show="!field.hidden">
                            <el-row>
                                <!-- Label Column -->
                                <el-col :span="caculateLabelSpan(field)">
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
                                <el-col :span="caculateFieldSpan(field)">
                                    <el-form-item 
                                        :prop="field.model" 
                                        v-show="!field.hidden">
                                        
                                        <template>
                                            <component
                                                :is="getFieldComponent(field)"
                                                v-bind="getFieldProps(field)"
                                                v-model="form[field.model]">
                                                <template v-if="['select', 'radio', 'checkbox'].includes(field.type)">
                                                    <template v-if="field.type === 'select'">
                                                        <template v-for="option in field.options" :key="option.value">
                                                            <el-option
                                                                :label="option.label"
                                                                :value="option.value" />
                                                        </template>
                                                    </template>
                                                    <template v-if="field.type === 'radio'">
                                                        <template v-for="option in field.options" :key="option.value">
                                                            <el-radio
                                                            :label="option.value">{{ option.label }}</el-radio>
                                                        </template>
                                                    </template>
                                                    <template v-if="field.type === 'checkbox'">
                                                        <template v-for="option in field.options" :key="option.value">
                                                            <el-checkbox
                                                                :label="option.label"
                                                                :value="option.value" />
                                                        </template>
                                                    </template>
                                                </template>
                                            </component>
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

    .el-form-item {
        margin-bottom: 0px;
    }
    
}

.form-body {
    margin-bottom: 3px;
}
</style>
