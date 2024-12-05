<template>
    <div style="height:100%; padding: 10px;">
        <!-- Actions Row -->
        <el-row style="margin-bottom: 10px;">
            <el-button v-if="user.checkPermission('add')" type="success" @click="onBtAdd">
                <el-icon><Plus /></el-icon> Add
            </el-button>
            <el-button v-if="user.checkPermission('delete')" type="danger" @click="onBtDelete">
                <el-icon><Delete /></el-icon> Delete
            </el-button>
            <el-button v-if="user.checkPermission('export')" type="primary" @click="onExport">
                <el-icon><Document /></el-icon> Export
            </el-button>
        </el-row>
        <!-- <div v-if="isLoading" class="loading-spinner">Loading...</div> -->
        <!-- Grade Table -->
        <ag-grid-vue 
            style="width: 100%; height: 80vh;" 
            class="table ag-theme-alpine" 
            :defaultColDef="agListTemplate.defaultColDef" 
            :rowHeight="30" 
            :columnDefs="agListTemplate.columnDefs" 
            :rowData="agListTemplate.rowData" 
            :pagination="true"
            :paginationPageSize="20" 
            :floatingFilter="true" 
            :rowSelection="agListTemplate.rowSelection" 
            :gridOptions="gridOptions" 
            :cellSelection="false" 
            :allowContextMenuWithControlKey="true" 
            @grid-ready="onGridReady" 
        />
    </div>
</template>

<script>
import { ref, reactive, onMounted, onBeforeUnmount } from "vue";
import { apiRequest } from "@/api/table";
//import { getGridData } from "@/api/table";
import { ElMessage } from "element-plus";
import useStore from "@/store";
import EventBus from "@/utils/eventBus";
import "ag-grid-enterprise";
import { Plus, Delete, Document } from "@element-plus/icons-vue";

export default {
    name: "ListTemplate",
    props: {
        schema: {
            type: Object,
            required: true
        }
    },
    components: {
        Plus,
        Delete,
        Document
    },
    setup(props) {
        const agListTemplate = reactive({
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
        const agData = ref([]);
        const user = useStore().user;
        const gridOptions = reactive({
            onCellDoubleClicked: (cell) => onCellDoubleClicked(cell),
        });

        // Fetch grid data
        const getData = async () => {
            isLoading.value = true;
            try {
                const payload = { type: "all" };
                console.log('Fetching data...', payload);
                const response = await apiRequest(props.schema.functions.list, payload);

                //const [columnDefs, rowData] = getGridData(response.data.items);
                const columnDefs = getColumnDef();
                console.log("columnDefs = ", columnDefs);
                console.log("response.data.items = ", response.data.items);
                
                agListTemplate.columnDefs = columnDefs;
                agListTemplate.rowData = response.data.items;
                agData.value = response.data.items;
            } catch (error) {
                console.error(error);
            } finally {
                isLoading.value = false;
            }
        };

        const getColumnDef = () => {
            let columnDefs = [];
            props.schema.fields.forEach(field => {
                let item = { 
                    field: field.column, 
                    headerName: field.column,
                    headerTooltip: field.column, 
                    filterParams: { applyMiniFilterWhileTyping: true }, 
                    autoHeight: true, 
                    wrapText: true,
                };
                if (field.hidden) {
                    item.hide = true;
                };
                columnDefs.push(item);
            });
            return columnDefs;
        };

        // Cell double-click handler
        const onCellDoubleClicked = (cell) => {
            if (!user.checkPermission("edit")) return;

            const rowData = { ...cell.data };

            const params = {
                options: "edit",
                comName: "FormTemplate",
                rowData,
            };
            EventBus.emit("passfunction", params);
        };

        const onBtAdd = () => {
            const rowData = {};
            const params = { options: "add", comName: "ListTemplate", rowData };
            EventBus.emit("passfunction", params);
        };

        const onBtDelete = async () => {
            const selectedRows = agListTemplate.gridApi.getSelectedRows();
            if (!selectedRows.length) {
                ElMessage.warn("No rows selected for deletion");
                return;
            }

            try {
                const deleteRowId = selectedRows.map((item) => item.GID).join(",");
                console.log("deleteRowId: ", deleteRowId);

                const payload = { 
                    id: deleteRowId,
                    mail: user.info.mail
                };
                console.log("payload = ", payload)
                const response = await apiRequest(props.schema.functions.delete, payload);
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
            const param = { fileName: props.schema.formName };
            agListTemplate.gridApi.exportDataAsExcel(param);
        };

        const onGridReady = (params) => {
            agListTemplate.gridApi = params.api;
            agListTemplate.columnApi = params.columnApi;
            agListTemplate.gridApi.sizeColumnsToFit();
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
            agListTemplate,
            agData,
            user,
            gridOptions,
            onBtAdd,
            onBtDelete,
            onExport,
            onGridReady,
            isLoading,
            Plus,
            Delete,
            Document
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
