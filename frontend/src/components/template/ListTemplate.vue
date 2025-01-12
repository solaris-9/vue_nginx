<script setup lang="ts">
import { ref, reactive, onMounted, onBeforeUnmount } from "vue";
import { ElMessage } from "element-plus";
import { Plus, Delete, Document } from "@element-plus/icons-vue";
import useStore from "@/store";
import EventBus from "@/utils/eventBus";
import { apiRequest } from "@/api/table";
import "ag-grid-enterprise";

// Props
const props = defineProps({
    schema: {
        type: Object,
        required: true
    }
});

// State
const user = useStore().user;
const mail = user.getUser().mail;
const keyColumn = ref("");
const rowData = ref([]);
const columnDefs = ref([]);
const isLoading = ref(true);
const gridOptions = reactive({
    onCellDoubleClicked: handleCellDoubleClick,
    autoSizeStrategy: {
        type: 'fitCellContents'
    },
});
const rowSelection = {mode: "multiRow"};
const defaultColDef = {
    menuTabs: ["filterMenuTab", "columnsMenuTab", "generalMenuTab"],
    sortable: true,
    filter: true,
    resizable: true,
};

const actions = [
    { name: "add", label: "Add", icon: Plus, type: "success", permission: "add", handler: handleAdd },
    { name: "delete", label: "Delete", icon: Delete, type: "danger", permission: "delete", handler: handleDelete },
    { name: "export", label: "Export", icon: Document, type: "primary", permission: "export", handler: handleExport }
];

function checkAction(action) {
    if (action.name === 'export') {
        return true;
    }
    return props.schema.functions[action.name] ? true : false
}

// Methods
async function fetchData() {
    isLoading.value = true;
    try {
        console.log('list api = ',  props.schema.functions.list)
        const response = await apiRequest(props.schema.functions.list, { type: "all" });
        columnDefs.value = generateColumnDefs();
        rowData.value = response.data.items;
    } catch (error) {
        console.error("Error fetching data:", error);
    } finally {
        isLoading.value = false;
    }
}

function generateColumnDefs() {
    // const resp = props.schema.fields
    //     .filter((field) => field.model)
    //     .map(field => ({
    //         field: field.model,
    //         headerName: field.column,
    //         headerTooltip: field.column,
    //         filterParams: { applyMiniFilterWhileTyping: true },
    //         autoHeight: true,
    //         wrapText: false,
    //         hide: field.listHidden || false,
    //     }));
    const resp = [];
    props.schema.fields.forEach(field => {
        if (field.model) {
            if (field.type === 'group') {
                field.fields.forEach(f => {
                    resp.push(
                        {
                            field: f.model,
                            headerName: f.column,
                            headerTooltip: f.column,
                            filterParams: { applyMiniFilterWhileTyping: true },
                            autoHeight: true,
                            wrapText: false,
                            hide: field.listHidden || false,
                        }        
                    );
                });
            } else {
                resp.push(
                    {
                        field: field.model,
                        headerName: field.column,
                        headerTooltip: field.column,
                        filterParams: { applyMiniFilterWhileTyping: true },
                        autoHeight: true,
                        wrapText: false,
                        hide: field.listHidden || false,
                    }        
                );
            }
        }
    });
    console.log("resp = ", resp)
    return resp
}

function handleCellDoubleClick(cell) {
    if (!user.checkPermission("edit")) return;

    //console.log(props.schema.functions);
    EventBus.emit(props.schema.notifications.switch, {
        options: "edit",
        comName: "FormTemplate",
        rowData: { ...cell.data }
    });
}

function handleAdd() {
    EventBus.emit(props.schema.notifications.switch, { options: "add", comName: "ListTemplate", rowData: {} });
}

async function handleDelete() {
    const selectedRows = gridOptions.api.getSelectedRows();
    console.log("selectedRows = ", selectedRows)
    if (!selectedRows.length) {
        ElMessage.warning("No rows selected for deletion");
        return;
    }

    try {
        const idsToDelete = selectedRows.map(row => row[keyColumn.value]).join(",");
        await apiRequest(props.schema.functions.delete, { id: idsToDelete, mail: mail });
        EventBus.emit(props.schema.notifications.refresh);
    } catch (error) {
        console.error("Error deleting rows:", error);
        ElMessage.error("Failed to delete records");
    }
}

function handleExport() {
    gridOptions.api.exportDataAsExcel({ fileName: props.schema.formName });
}

function onGridReady(params) {
    gridOptions.api = params.api;
    gridOptions.columnApi = params.columnApi;
    params.api.sizeColumnsToFit();
}

function getKeyColumn() {
    const fieldWithKey  = props.schema.fields.find((field) => field.key === true);
    keyColumn.value = fieldWithKey ? fieldWithKey.model : "";
    console.log("keyColumn = ", keyColumn.value)
}

// Lifecycle Hooks
onMounted(() => {
    EventBus.on(props.schema.notifications.refresh, fetchData);
    fetchData();
    getKeyColumn();
    if (props.schema.skipAutoResize) {
        gridOptions.autoSizeStrategy.type = "fitProvidedWidth";
    }
    console.log("gridOptions = ", gridOptions)
});

onBeforeUnmount(() => {
    EventBus.off(props.schema.notifications.refresh, fetchData);
});
</script>

<template>
    <div class="list-template">
        <!-- Actions Row -->
        <el-row class="action-buttons">
            <template v-for="action in actions" :key="action.name">
                <el-button
                    v-if="user.checkPermission(action.permission) && checkAction(action)"
                    :type="action.type"
                    @click="action.handler"
                >
                    <el-icon>
                        <component :is="action.icon" />
                    </el-icon> 
                    {{ action.label }}
                    </el-button>
            </template>
        </el-row>

        <!-- Grade Table -->
        <ag-grid-vue 
            class="table ag-theme-alpine"
            style="width: 100%; height: 80vh;" 
            :defaultColDef="defaultColDef"
            :rowHeight="30" 
            :columnDefs="columnDefs" 
            :rowData="rowData" 
            :pagination="true"
            :paginationAutoPageSize="true" 
            :floatingFilter="true" 
            :rowSelection="rowSelection" 
            :gridOptions="gridOptions" 
            @grid-ready="onGridReady"
            :loading="isLoading"
        />
    </div>
</template>


<style scoped>
.list-template {
    /* height: 100%; */
    height: calc(100vh - 155px);
    padding: 10px;
}
.action-buttons {
    margin-bottom: 10px;
}
.table {
    width: 100%;
    height: 80vh;
}
</style>
