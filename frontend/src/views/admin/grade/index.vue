
<template>
    <div  class="app-container">
      <Transition name="fade" mode="out-in">
        <keep-alive include="GradeManagement">  
            <component :is="comName" :fromData="fromData" :fromrules="fromrules" :fromTitle="fromTitle" @passfunction="show_component"></component>
        </keep-alive>
      </Transition>
    </div>
</template>
    <script>
    import GradeManagement from "./grade"
    //import fromTemp from "@/views/customer-info/components/from-temp"
    import { getUserName } from '@/utils/auth'
    import { getCustomer } from '@/utils/table'
    import { 
      getFormItemTitle,
      formSettingRule,
      requestAPI
    } from "@/utils/forms"
    
    export default {
      data() {
        return {
          comName: "GradeManagement",
          username: null,
          fromData: {},
          fromrules: {},
          fromTitle: {},
          options: [],
          certificatesList: [],
        }
      },
      components: {GradeManagement},
      computed: {
       
      },
      watch: {
      },
      created() {
        this.username = getUserName()
        getCustomer().then( res=>{
          this.options = res
        })
    
      },
      methods: {
        // show component
        show_component(params){
          // 切换动态组件
          if(params.submit){
            this.updateTable(params)
            return
          }
    
        //   this.comName = (this.comName==="fromTemp")?params.comName:"fromTemp"
        //   if(this.comName==="fromTemp"){  //切换动态组件,当切到fromTemp时
        //     let FromRequired = ["Grade", "Add", "Edit" ,"Delete", "Search", "View", "Export", "Download"]  //from rule是必选项的item
        //     let rules = formSettingRule(params.rowData, FromRequired)  //from表单rule
    
        //     // fromTitle配置,默认为edit的fromTitle
        //     let fromTitle = { 
        //       "ID": getFormItemTitle("hide"),
        //     }  
        //     let selectList = ["Add", "Edit" ,"Delete", "Search", "View", "Export", "Download"]
        //     selectList.forEach((item)=>{
        //       let titleData = getFormItemTitle("select")
        //       titleData.choiceList = ["Yes", "No"]
        //       titleData.multiple = false
        //       fromTitle[item] = titleData
        //     })
  
        //     if(params.options==="add"){ //add添加的时候，调整fromTitle
              
        //     }
    
        //     this.fromData = params
        //     this.fromrules = rules
        //     this.fromTitle = fromTitle
        //     this.$forceUpdate() 
        //   }else{  //切换动态组件，当切到product table时，将add或edit的表数据更新到表格中
            this.fromData = params
        //   }
          
        },
        // call api to implement add and edit
        async updateTable(fromDataParam){
          let url = "api/user/grade_edit", update_params = { "type": "2", ...fromDataParam.rowData}
          // Obtain interface parameters
          if(fromDataParam.options==="add"){update_params.type="1"}
          
          let notify_info = await requestAPI(url, update_params, fromDataParam.options, true)
          if(notify_info.type==="success"){
            this.$bus.$emit('refreshGradeTable')
          }
        },
      }
    }
    </script>
    
    <style scoped>
      .tab-container {
        margin: 30px 10px 10px 20px;
      }
    </style>