<template>
    <div class="app-container">
        <Transition name="fade-transform" mode="out-in">
            <keep-alive include="ListTemplate">
                <ListTemplate 
                    v-if="formIndicator === 'nwcclist'"
                    :key="getCompKey('nwcc')"
                    @notification="handleComponentChange"
                    :formType="formType"
                    :formData="formData"
                    :schema="nwcc"
                />
                <FormTemplate 
                    v-else-if="formIndicator === 'nwccedit' || formIndicator === 'nwccadd'"
                    :key="getCompKey('nwcc')"
                    @notification="handleComponentChange"
                    :formType="formType"
                    :formData="formData"
                    :schema="nwcc"
                />
                <FormTemplate 
                    v-else
                    :key="getCompKey('devicedp')"
                    @notification="handleComponentChange"
                    :formType="formType"
                    :formData="formData"
                    :schema="devicedp"
                />
            </keep-alive>
        </Transition>
    </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from "vue";
import FormTemplate from "@/components/template/FormTemplate.vue";
import ListTemplate from "@/components/template/ListTemplate.vue";
import useStore from "@/store";
import EventBus from "@/utils/eventBus";
import devicedp from "./devicedp.json";
import nwcc from "./nwcc.json";
// import ListTemplate from "../../components/template/ListTemplate.vue";
// import FormTemplate from "../../components/template/FormTemplate.vue";
// import FormTemplate from "../../components/template/FormTemplate.vue";

export default {
    name: "LandingTemplate",

    components: { ListTemplate, FormTemplate },

    props: {
        schema: {
            type: Object,
            required: true
        }
    },

    setup(props) {
        const comName = ref("ListTemplate");
        const userName = ref("");
        const formData = reactive({});
        const formType = ref("");
        const formIndicator = ref("nwcclist")
        const user = useStore().user;
        const componentKey = ref(`${props.schema.comName}-${Math.random().toString(36).slice(2, 11)}`);
        const schema = reactive(props.schema);
        const notification = ref(props.schema.notifications.switch);

        const getCompKey = (com) => {
            switch (com) {
                case 'nwcc':
                    return `NWCC-${Math.random().toString(36).slice(2, 11)}`;
                case 'devicedp':
                    return `DEVICEDP-${Math.random().toString(36).slice(2, 11)}`;
            }
        };

        const handleComponentChange = (params) => {
            if (!params || !params.options) {
                console.warn("Invalid parameters received:", params);
                return;
            }

            const { options, rowData } = params;
            console.log('handleComponentChange ', params)
            switch (options) {
                case "add":
                    //comName.value = "FormTemplate";
                    formType.value = "add";
                    formIndicator.value = "nwccadd"
                    Object.keys(formData).forEach((key) => delete formData[key]);
                    break;
                case "edit":
                    //comName.value = "FormTemplate";
                    formType.value = "edit";
                    formIndicator.value = "nwccedit"
                    Object.assign(formData, rowData || {});
                    break;
                case "add-device":
                    //comName.value = "FormTemplate";
                    formType.value = "add";
                    formIndicator.value = "devicedpadd"
                    console.log('rowData = ', rowData)
                    Object.keys(formData).forEach((key) => delete formData[key]);
                    Object.assign(formData, rowData || {});
                    //Object.assign(schema, devicedp);
                    //componentKey.value = `form-${Math.random().toString(36).slice(2, 11)}`; // Force re-render
                    break;
                case "list":
                default:
                    //comName.value = "ListTemplate";
                    console.log("using nwcc schema")
                    formIndicator.value = "nwcclist"
                    //setTimeout(() => {
                    //    Object.assign(schema, nwcc);
                    //    componentKey.value = `form-${Math.random().toString(36).slice(2, 11)}`; // Force re-render
                    //}, 0);
                    break;
            }
            console.log('handleComponentChange ', formIndicator.value)
        };

        onMounted(() => {
            userName.value = user.getUser().name;
            EventBus.on(notification.value, handleComponentChange);
        });

        onBeforeUnmount(() => {
            EventBus.off(notification.value, handleComponentChange);
        });

        return {
            comName,
            userName,
            formData,
            formType,
            handleComponentChange,
            componentKey,
            schema,
            formIndicator,
            getCompKey,
            nwcc,
            devicedp
        };
    },
};
</script>

<style scoped>
.tab-container {
    margin: 2px 2px 0px 0px;
}
</style>
