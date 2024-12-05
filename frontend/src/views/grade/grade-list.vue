<template>
    <div style="height:100%; padding: 10px;">
        <!-- Actions Row -->
        <el-row style="margin-bottom: 10px;">
            <el-button v-if="user.checkPermission('add')" type="success" @click="onBtAdd">
                <i class="el-icon-plus" /> Add
            </el-button>
            <el-button v-if="user.checkPermission('delete')" type="danger" @click="onBtDelete">
                <i class="el-icon-delete" /> Delete
            </el-button>
            <el-button v-if="user.checkPermission('export')" type="primary" @click="onExport">
                <svg-icon icon-class="excel" /> Export
            </el-button>
        </el-row>
        <!-- <div v-if="isLoading" class="loading-spinner">Loading...</div> -->
        <!-- Grade Table -->
        <ag-grid-vue style="width: 100%; height: 80vh;" class="table ag-theme-alpine" :defaultColDef="agGridGradeManagement.defaultColDef" :rowHeight="30" :columnDefs="agGridGradeManagement.columnDefs" :rowData="agGridGradeManagement.rowData" :pagination="true"
            :paginationPageSize="20" :floatingFilter="true" :rowSelection="agGridGradeManagement.rowSelection" :gridOptions="gridOptions" :cellSelection="false" :allowContextMenuWithControlKey="true" @grid-ready="onGridReady" />
    </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from "vue";
import { apiRequest } from "@/api/table";
import { getGridData } from "@/api/table";
import { ElMessage } from "element-plus";
import useStore from "@/store";
import EventBus from "@/utils/eventBus";
import "ag-grid-enterprise";

export default {
    name: "GradeList",
    setup() {
        const agGridGradeManagement = reactive({
            gridApi: null,
            columnApi: null,
            rowSelection: { mode: "multiRow" },
            defaultColDef: {
                menuTabs: ["filterMenuTab", "columnsMenuTab", "generalMenuTab"],
                sortable: true,
                filter: true,
                resizable: true,
            },
            columnDefs: null,
            rowData: null,
        });
        const isLoading = ref(true);
        const gradeManagementOrigin = ref([]);
        const user = useStore().user;
        const gridOptions = reactive({
            onCellDoubleClicked: (cell) => onCellDoubleClicked(cell),
        });

        // Fetch grid data
        const getData = async () => {
            isLoading.value = true;
            try {
                
                let payload = { type: "all" };
                console.log('Fetching data...', payload);
                const response = await apiRequest("gradeList", payload);
                const [columnDefs, rowData] = getGridData(response.data.items);
                agGridGradeManagement.columnDefs = columnDefs;
                agGridGradeManagement.rowData = rowData;
                gradeManagementOrigin.value = response.data.items;
            } catch (error) {
                console.error(error);
            } finally {
                isLoading.value = false;
            }
        };

        // Cell double-click handler
        const onCellDoubleClicked = (cell) => {
            if (!user.checkPermission("edit")) return;

            const rowData = { ...cell.data };

            const params = {
                options: "edit",
                comName: "GradeForm",
                rowData,
            };
            EventBus.emit("passfunction", params);
        };

        const onBtAdd = () => {
            const rowData = {};
            const params = { options: "add", comName: "GradeList", rowData };
            EventBus.emit("passfunction", params);
        };

        const onBtDelete = async () => {
            const selectedRows = agGridGradeManagement.gridApi.getSelectedRows();
            if (!selectedRows.length) {
                ElMessage.warn("No rows selected for deletion");
                return;
            }

            try {

                const deleteRowId = selectedRows.map((item) => item.GID).join(",");
                console.log("deleteRowId: ", deleteRowId);

                // const method = "post"
                // const url = "api/admin/grade_delete"
                const payload = { 
                    id: deleteRowId,
                    mail: user.info.mail
                };
                console.log("payload = ", payload)

                // const response = await axios({
                //     method,
                //     url: url,
                //     data: payload
                // });
                const response = await apiRequest("gradeDelete", payload);
                console.log("API response: ", response);

                EventBus.emit("refreshGradeTable", {});
            } catch (error) {
                console.log("API failed: ", error);
                ElMessage.error(
                    "Record deletion failed!"
                );
            };
        };

        const onExport = () => {
            const param = { fileName: "gradeManagement" };
            agGridGradeManagement.gridApi.exportDataAsExcel(param);
        };

        const onGridReady = (params) => {
            agGridGradeManagement.gridApi = params.api;
            agGridGradeManagement.columnApi = params.columnApi;
            agGridGradeManagement.gridApi.sizeColumnsToFit();
        };

        onMounted(() => {
            console.log("onMounted ...")
            //console.log(route.name);
            EventBus.on("refreshGradeTable", getData);
            getData();
        });

        onBeforeUnmount(() => {
            EventBus.off("refreshGradeTable", getData);
        });

        return {
            agGridGradeManagement,
            gradeManagementOrigin,
            user,
            gridOptions,
            onBtAdd,
            onBtDelete,
            onExport,
            onGridReady,
            isLoading
        };
    },
};
</script>

<style scoped>
.el-popover .el-button:hover {
    color: blue;
    font-weight: 1000;
}

.filter-item {
    margin: 0px 10px;
}
</style>
