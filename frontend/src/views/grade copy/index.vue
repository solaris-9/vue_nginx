<template>
    <div class="app-container">
        <Transition name="fade-transform" mode="out-in">
            <keep-alive include="GradeList">
                <component :is="comName" :formdata="formdata" :formrules="formrules" :formtype="formtype" @passfunction="show_component" />
            </keep-alive>
        </Transition>
    </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from "vue";
import GradeList from "./grade-list.vue";
import GradeForm from "./grade-form.vue";
import useStore from "@/store";
import EventBus from "@/utils/eventBus";

export default {
    name: "DynamicComponentManager",
    components: { GradeList, GradeForm },

    setup() {
        // Reactive state
        const comName = ref("GradeList");
        const username = ref(null);
        const formdata = reactive({});
        const formrules = reactive({});
        const formtype = ref("");
        const options = ref([]);
        const certificatesList = ref([]);
        const user = useStore().user;

        // Method to handle `passfunction` events
        const show_component = (params) => {
            console.log("Received params in show_component:", params);

            // Example logic for component switching
            if (params && params.options === "add") {
                comName.value = "GradeForm";
                formtype.value = "add";
                //Object.assign(formdata, {});
                //formdata = reactive({});
                // Object.keys(formdata).forEach((key) => {
                //   delete formdata[key];
                // });
                console.log('formdata: ', formdata);
            } else if (params && params.options === "list") {
                comName.value = "GradeList";
            } else if (params && params.options === "edit") {
                comName.value = "GradeForm";
                formtype.value = "edit";
                Object.assign(formdata, params.rowData || {});
                console.log(formdata);
            }
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
            formrules,
            formtype,
            options,
            certificatesList,
            show_component,
        };
    },
};
</script>

<style scoped>
.tab-container {
    margin: 30px 10px 10px 20px;
}
</style>
