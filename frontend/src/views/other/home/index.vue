<template>
  <!-- home page, prompt system information -->
  <transition name="el-zoom-in-center">  
    <div style="height: 100%;padding: 30px;text-align: center;">  
      <div style="height: 100%;width: 100%;display: inline-block;margin-top: 5%;">
        <!-- information title -->
        <span style="display: inline-block;width: 100%;font-size: 60px;font-weight: 600;color: #005aff;">
          <span style="display: block;">BBD Device Deployment Tool</span>
          
        </span>
        <!-- Prompt the initial page information according to the level status -->
        <span style="display: inline-block;width: 100%;margin-top: 15%;font-size: 20px;">
          <span v-if="levelStatus">
            Facilitate your work and improve work efficiency of BBD.
          </span> 
          <span v-else style="color: #000;">
            <span style="display: block;">Sorry, you don’t have access authority, if you need access, please mail </span>
            <span style="display: block;">
              <span style="display: inline-block;color:#005aff;cursor: pointer;" ref="copytext" @click="copyText($refs.copytext.innerText)" title="click, and copy email address">dandan.yu@nokia-sbell.com</span>  
              to apply, Thanks for your cooperation.
            </span>
          </span>
        </span> 
        
      </div>
    </div>
</transition>
</template>
  
<script>
import store from "@/store"

export default {
  name: "ManufactortSW",
  directives: {},
  components: {},
  data() {
    return {
    }
  },
  computed:{
    levelStatus(){
      return !(['', '1', undefined, null, 0, "0"].includes(store.getters.level))
    }  
  },
  created() {
  },
  methods: {
    /**
     * @description: copy specified content 
     * @param {String} text copied content 
     * @return void
     */
    copyText(text){
      var input = document.createElement("input") // 创建input对象
     input.value = text // 设置复制内容
     document.body.appendChild(input) // 添加临时实例
     input.select() // 选择实例内容
     document.execCommand("Copy") // 执行复制
     document.body.removeChild(input) // 删除临时实例
     this.$message.success('copy the email address success！')
    },
  }
}
</script>
<style scoped>
html, body, #app{
    margin: 0;
    height: 100%;
    width: 100%;
    padding: 0;
  }

</style>
