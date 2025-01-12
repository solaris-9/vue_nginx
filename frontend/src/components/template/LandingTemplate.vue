<template>
    <div class="app-container">
        <Transition name="fade-transform" mode="out-in">
            <keep-alive include="ListTemplate">
                <component 
                    :is="comName" 
                    :key="componentKey"
                    :formData="formData" 
                    :formType="formType" 
                    @notification="handleComponentChange"
                    :schema="schema"
                />
            </keep-alive>
        </Transition>
    </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from "vue";
import FormTemplate from "./FormTemplate.vue";
import ListTemplate from "./ListTemplate.vue";
import useStore from "@/store";
import EventBus from "@/utils/eventBus";

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
        const user = useStore().user;
        const componentKey = ref(`${props.schema.comName}-${Math.random().toString(36).slice(2, 11)}`);
        const schema = reactive(props.schema);
        const notification = ref(props.schema.notifications.switch);

        const handleComponentChange = (params) => {
            if (!params || !params.options) {
                console.warn("Invalid parameters received:", params);
                return;
            }

            const { options, rowData } = params;
            switch (options) {
                case "add":
                    comName.value = "FormTemplate";
                    formType.value = "add";
                    Object.keys(formData).forEach((key) => delete formData[key]);
                    break;
                case "edit":
                    comName.value = "FormTemplate";
                    formType.value = "edit";
                    Object.assign(formData, rowData || {});
                    break;
                case "list":
                default:
                    comName.value = "ListTemplate";
                    break;
            }
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
            schema
        };
    },
};
</script>

<style scoped>
.tab-container {
    margin: 2px 2px 0px 0px;
}
</style>
