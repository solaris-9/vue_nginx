<template>
    <div class="app-container">
        <Transition name="fade-transform" mode="out-in">
            <keep-alive include="ListTemplate">
                <component 
                    :is="comName" 
                    :key="comName + key"
                    :formdata="formdata" 
                    :formtype="formtype" 
                    @passfunction="show_component"
                    :schema="grade"
                />
            </keep-alive>
        </Transition>
    </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from "vue";
//import ListTemplate from "./grade-list.vue";
//import GradeForm from "./grade-form.vue";
import FormTemplate from "@/components/template/FormTemplate.vue";
import ListTemplate from "@/components/template/ListTemplate.vue";
import useStore from "@/store";
import EventBus from "@/utils/eventBus";
import grade from "./grade.json";

export default {
    name: "GradeMain",
    components: { ListTemplate, FormTemplate },

    setup() {
        // Reactive state
        const comName = ref("ListTemplate");
        const username = ref(null);
        const formdata = reactive({});
        const formtype = ref("");
        const options = ref([]);
        const user = useStore().user;
        const key = ref("-" + (Math.random() * 1e10))

        // Method to handle `passfunction` events
        const show_component = (params) => {
            console.log("Received params in show_component:", params);
            if (!params || !params.options) {
                console.warn("Invalid parameters received:", params);
                return;
            }

            // Example logic for component switching
            if (params && params.options === "add") {
                comName.value = "FormTemplate";
                formtype.value = "add";
                Object.keys(formdata).forEach((key) => delete formdata[key]);
                //Object.assign(formdata, {});
                //formdata = reactive({});
                // Object.keys(formdata).forEach((key) => {
                //   delete formdata[key];
                // });
                console.log('formdata: ', formdata);
            } else if (params && params.options === "list") {
                comName.value = "ListTemplate";
            } else if (params && params.options === "edit") {
                comName.value = "FormTemplate";
                formtype.value = "edit";
                Object.assign(formdata, params.rowData || {});
                console.log(formdata);
            };

            //console.log("tooltip ========= ", document.querySelectorAll(".el-tooltip"));

        };

        // Lifecycle hooks
        onMounted(() => {
            username.value = user.getUser().name;
            EventBus.on("passfunction", show_component); // Register EventBus listener
        });

        onBeforeUnmount(() => {
            EventBus.off("passfunction", show_component); // Clean up listener
        });

        return {
            comName,
            username,
            formdata,
            formtype,
            options,
            show_component,
            grade,
            key
        };
    },
};
</script>

<style scoped>
.tab-container {
    margin: 30px 10px 10px 20px;
}
</style>
