<template>
    <div class="tab-container">
        <el-form ref="formRef" :model="form" label-width="120px">
            <el-input v-model="form.gid" type="hidden" />
            <el-form-item label="Grade">
                <el-input v-model="form.grade" style="width: 240px" />
            </el-form-item>
            <el-form-item label="Add">
                <el-select v-model="form.add" placeholder="Select" style="width: 240px">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </el-form-item>
            <el-form-item label="Edit">
                <el-select v-model="form.edit" placeholder="Select" style="width: 240px">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </el-form-item>
            <el-form-item label="Delete">
                <el-select v-model="form.delete" placeholder="Select" style="width: 240px">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </el-form-item>
            <el-form-item label="Search">
                <el-select v-model="form.search" placeholder="Select" style="width: 240px">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </el-form-item>
            <el-form-item label="View">
                <el-select v-model="form.view" placeholder="Select" style="width: 240px">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </el-form-item>
            <el-form-item label="Export">
                <el-select v-model="form.export" placeholder="Select" style="width: 240px">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </el-form-item>
            <el-form-item label="Download">
                <el-select v-model="form.download" placeholder="Select" style="width: 240px">
                    <el-option v-for="item in options" :key="item.value" :label="item.label" :value="item.value" />
                </el-select>
            </el-form-item>
    
            <el-form-item>
                <el-button type="primary" @click="onSubmit">Submit</el-button>
                <el-button @click="onCancel">Cancel</el-button>
            </el-form-item>
        </el-form>
    </div>
</template>
  
  
<script>
import { reactive, ref, watch, onMounted, toRef } from "vue";
import { ElMessage } from "element-plus";
import EventBus from "@/utils/eventBus";
//import axios from "axios";
import useStore from "@/store";
import { gradeEdit, gradeAdd } from "@/api/table";

export default {
    name: "GradeForm",
    props: {
        formdata: {
            type: Object,
            default: () => ({}),
        },
        formtype: {
            type: String,
            required: true
        },
    },
    setup(props) {
        const formRef = ref(null);

        //const id = ref(null);
        // Reactive form data
        const form = reactive({
            gid: "",
            grade: "",
            add: "",
            edit: "",
            delete: "",
            search: "",
            view: "",
            export: "",
            download: "",
        });

        const options = [{
                value: 'Yes',
                label: 'Yes'
            },
            {
                value: 'No',
                label: 'No'
            },
        ];

        // Reset the form to blank values
        const resetForm = () => {
            form.gid = "";
            form.grade = "";
            form.add = "No";
            form.edit = "No";
            form.delete = "No";
            form.search = "No";
            form.view = "Yes";
            form.export = "No";
            form.download = "No";
        };

        const user = useStore().user;

        // Watch for changes in `formdata` and update `form`
        watch(
            () => props.formdata,
            (newData, oldData) => {
                console.log("New formData received:", newData); // Debug: Log new data
                console.log("Previous formData:", oldData); // Debug: Log old data
                console.log("formtype: ", props.formtype);
                //console.log("length: ", Object.keys(newData))
                if (props.formtype === "edit") {
                    if (newData && Object.keys(newData).length > 0) {
                        console.log("Populating form with newData..."); // Debug: Log action
                        //Object.assign(form, newData); // Populate form with formData values
                        Object.keys(newData).forEach((key) => {
                            let lkey = key.toLowerCase();
                            if (lkey in form) {
                                form[lkey] = newData[key];
                            } else if (lkey === "gid") {
                                id.value = newData[key];
                            }
                        });
                        console.log("form value: ", form)
                    }
                } else if (props.formtype === "add") {
                    console.log("Form in add mode, resetting form ...")
                    resetForm();
                };
            }, 
            { immediate: true }
        );

        const onSubmit = async () => {
            //ElMessage.success("Submit!");
            console.log("Submitted data:", form);
            try {
                // const method = form.gid ? "put" : "post";
                // const url = "api/admin/grade_edit"
                let payload = { ...form };
                //console.log("user info: ", user.info.mail)
                payload.mail = user.info.mail;
                console.log("payload = ", payload)
                // const response = await axios({
                //     method,
                //     url: url,
                //     data: payload
                // });
                let response = undefined;
                if (form.gid) {
                    response = await gradeEdit(payload);
                } else {
                    response = await gradeAdd(payload);
                }
                console.log("API response: ", response.data);

                ElMessage.success(
                    form.gid ? "Record updated successfully!" : "Record created successfully!"
                );

                EventBus.emit("passfunction", {
                    options: "list",
                    comName: "GradeList",
                });
                EventBus.emit("refreshGradeTable", {});
            } catch (error) {
                console.log("API failed: ", error);
                ElMessage.error(
                    form.gid ? "Record updated failed!" : "Record created failed!"
                );
            }

        };

        const onCancel = () => {
            resetForm(); // Reset form on cancel
            const params = {
                options: "list",
                comName: "GradeList",
            };
            EventBus.emit("passfunction", params);
        };

        onMounted(() => {
            console.log("Component mounted, form initialized");
            //console.log(this.formdata)
        });

        return {
            form,
            formRef,
            onSubmit,
            onCancel,
            //id,
            options
        };
    },
};
</script>
  
  
  
<style scoped>
.tab-container {
    margin: 30px;
}
</style>
  