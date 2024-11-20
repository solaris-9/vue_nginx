<template>
  <div style="height:100%;padding: 10px;">   
      <el-row style="margin-bottom: 10px;">
          <!-- add data -->
          <el-button v-if="$checkPermission('GradeManagement', 'add')" type="success" @click="onBtAdd">
            <i class="el-icon-plus" />
            Add
          </el-button>
          <!-- <el-button type="danger" @click="onBtDelete">
            <i class="el-icon-delete" />
            Delete
          </el-button> -->
          <!-- excel export data -->
          <el-button v-if="$checkPermission('GradeManagement', 'export')" type="primary" @click="onExport">
            <svg-icon icon-class="excel" />
            Export
          </el-button>
      </el-row>
      <!-- grade ag-grid table -->
      <ag-grid-vue
          style="width: 100%; height: 80vh;"
          class="table ag-theme-alpine"
          :defaultColDef="agGridGradeManagement.defaultColDef"
          :rowHeight="30"
          :column-defs="agGridGradeManagement.columnDefs"
          :row-data="agGridGradeManagement.rowData"
          :pagination="true"
          :pagination-page-size="20"
          :floating-filter="true"
          :rowSelection="agGridGradeManagement.rowSelection"
          :gridOptions="gridOptions"
          :enableRangeSelection="true"
          :allowContextMenuWithControlKey="true"
          :getContextMenuItems="$getContextMenuItems"
          @grid-ready="onGridReady"
      />

  </div>
</template>

<script>
import {adminGradeManagement} from "@/api/table"
import {getGridData} from "@/utils/table"
import { 
  getFormItemTitle,
  formSettingRule,
  requestAPI
} from "@/utils/forms"
import axios from "axios"
import store from "@/store"

export default {
  name: "GradeManagement",
  directives: {},
  components: {},
  data() {
    return {
      gridOptions : {
        // suppressContextMenu: true, // forbid context menu
        onCellDoubleClicked: this.onCellDoubleClicked, //ag-grid table double click event
      },
      agGridGradeManagement: {
          gridApi: undefined,
          columnApi: undefined,
          rowSelection: 'multiple',
          defaultColDef: {
              // flex: 1,
              menuTabs: ['filterMenuTab', 'columnsMenuTab', 'generalMenuTab'], 
              sortable: true,
              filter: true,
              resizable: true,
          },
          columnDefs: null,
          rowData: null,
      },
      gradeManagementOrigin: [],
    }
  },
  mounted() {
    // bus sibling page method call
    this.$bus.$on('refreshGradeTable', (data)=>{
      this.getData()
    })
  },
  created() {
    this.getData()
  },
  beforeDestroy () {
    this.$bus.$off('refreshGradeTable', (data)=>{
      console.log(data)
    });
  },
  methods: {
    /**
     * @description: get adminGradeManagement table data
     * @return void
     */
    getData() {
      adminGradeManagement({Grade: "all"}).then( response =>{ // adminGradeManagement API interface
          [this.agGridGradeManagement.columnDefs, this.agGridGradeManagement.rowData] = getGridData(response.data.items)
          this.gradeManagementOrigin = response.data.items
      }).catch(error => {
          console.log(error)
      })
    },
    // add a grade
    onBtAdd(){
      let rowData = {}
      let deletedItem = ["Businessline", "Latest use", "ID"]
      Object.keys(this.gradeManagementOrigin[0]).forEach(key=>{
        if(!(deletedItem.some(i => i===key))){
          rowData[key] = ""
        }
      })
      let params = {"options": "add", "comName": "GradeManagement", "rowData": rowData}
      this.$emit("passfunction", params)
    },
    // edit a grade
    onCellDoubleClicked(cell){
      // premission control
      let permission = this.$checkPermission('GradeManagement', 'edit')
        if(!permission){
          return
        }

      // edit option
      let deletedItem = ["Businessline", "Latest use"]
      let rowData = JSON.parse(JSON.stringify(cell.data))
      deletedItem.forEach(item => {
        if(Object.keys(rowData).some(i => i===item)){
          this.$delete(rowData, item)
        }
      })
      let params = {"options": "edit", "comName": "GradeManagement", "rowData": rowData}
      this.$emit("passfunction", params)
    },
    // delete grades
    async onBtDelete(){
      let url = "", update_params = { "type": "3", "username": "xiama"}
      let getSelectedRows = this.agGridGradeManagement.gridApi.getSelectedRows() 
      let deleteRowId = "" 

      deleteRowId = getSelectedRows.map(item=> item.id).join(",")
      Object.assign(update_params, {"id": deleteRowId})

      if(getSelectedRows.length>0){  
        let notify_info = await requestAPI(url, update_params, "delete")
        if(notify_info.type==="success"){
          refreshTableData(tableName)
        }
        this.$notify({
            title: notify_info.title,
            message: notify_info.msg,
            type: notify_info.type,
            duration: 2000
        })  
      }else{
        this.$message({
          message: 'You haven\'t checked any rows in the Golden Info table that you want to delete yet',
          type: 'warning'
        })
      }
    },

    // ag-grid创建完成后执行的事件
    onGridReady(params) {
      // 获取gridApi
      this.agGridGradeManagement.gridApi = params.api
      this.agGridGradeManagement.columnApi = params.columnApi
      // 这时就可以通过gridApi调用ag-grid的传统方法了
      this.agGridGradeManagement.gridApi.sizeColumnsToFit()
    },
    // export grade table
    onExport(){
      let param = {
          fileName:'gradeManagement',
      }
      this.agGridGradeManagement.gridApi.exportDataAsExcel(param)
    },  
  }
}
</script>
<style scoped>
.el-popover .el-button:hover{
  color: blue;
  font-weight: 1000;
}
.filter-item{
  margin: 0px 10px;
}
</style>
