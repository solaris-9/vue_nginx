<template>
  <div class="login-container">
    <div class="login-left">
    </div>
    <div class="login-right">
      <div class="login-form-top">
      </div>
      
      <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on" label-position="left">
        <div class="title-container">
            <img class="title" src="@/assets/customer_images/nokia_logo.png" style="height: 30px;width: 120px;">
        </div>
        <el-form-item prop="username" style="background-color: transparent;">
          <span class="svg-container">
            <svg-icon icon-class="user" />
                <!-- <font-awesome-icon :icon="['fas','user']" /> -->
          </span>
          <el-input
            ref="username"
            v-model="loginForm.username"
            placeholder="Username"
            name="username"
            type="text"
            tabindex="1"
            autocomplete="off"
            style="color: #005aff;"
          />
        </el-form-item>
        <el-form-item prop="password"  style="background-color: transparent;">
          <span class="svg-container">
            <svg-icon icon-class="password" />
          </span>
          <el-input
            :key="passwordType"
            ref="password"
            v-model="loginForm.password"
            :type="passwordType"
            placeholder="Password"
            name="password"
            tabindex="2"
            autocomplete="off"
            @keyup.enter.native="handleLogin"
          />
          <span class="show-pwd" @click="showPwd">
            <svg-icon :icon-class="passwordType === 'password' ? 'eye' : 'eye-open'" />
          </span>
        </el-form-item>

          <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:30px;background: linear-gradient(to bottom right, #005aff, rgb(134, 22, 83));" @click.native.prevent="handleLogin">
            Login Device Deployment Tool
          </el-button>

        <div class="tips">

        </div>

      </el-form>

      <div class="login-form-bottom">
        <div style="margin-bottom: 0px;">
          <div>
            <p style="text-align: center;margin-top: 50px;color: #ffffff;">@Copy right Nokia 2023</p>
          </div>
        </div> 
      </div>
    </div>
    
  </div>
</template>

<script>
import { validUsername } from '@/utils/validate'
import { ElMessageBox } from 'element-plus'

export default {
  name: 'Login',
  data() {
    const validateUsername = (rule, value, callback) => {
      if (!validUsername(value)) {
        callback(new Error('Please enter the correct user name'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: '',
        password: ''
      },
      loginRules: {
        username: [{ required: true, trigger: 'blur', validator: validateUsername }],
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false,
      passwordType: 'password',
      redirect: undefined
    }
  },
  watch: {
    $route: {
      handler: function(route) {
        this.redirect = route.query && route.query.redirect
      },
      immediate: true
    }
  },
  methods: {
    showPwd() {
      if (this.passwordType === 'password') {
        this.passwordType = ''
      } else {
        this.passwordType = 'password'
      }
      this.$nextTick(() => {
        this.$refs.password.focus()
      })
    },
    handleLogin() {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          this.$store.dispatch('user/login', this.loginForm).then(() => {
             this.$router.push({ path: this.redirect || '/' })
            this.loading = false
          }).catch((error) => {
            this.$message.error('Authentication failed. Caught exception.' + error.message ); // 显示错误信息  
            this.loading = false
          })
        } 
        else {
          console.log('login error submit!!')
          // this.$message.error('Input error. Please see error on the page' ); // 显示错误信息 
          ElMessageBox.alert('Input error. Please see error on the page', 'Log in Failure', {  
                    confirmButtonText: 'OK',  
                    type: 'warning'  
                    });
          return false
        }
      })
    }
  }
}
</script>

<style lang="scss">

$bg:#000000;
$light_gray:#fff;
$cursor: #fff;

@supports (-webkit-mask: none) and (not (cater-color: $cursor)) {
  .login-container .el-input input {
    color: $cursor;
  }
}

/* reset element-ui css */
.login-container {
  .el-input {
    display: inline-block;
    height: 47px;
    width: 85%;
    min-width: 200px;

        
    input {
      background: transparent;
      border: 0px;
      -webkit-appearance: none;
      border-radius: 0px;
      padding: 12px 5px 12px 15px;
      height: 47px;
      caret-color: $cursor;

      &:-webkit-autofill {
        box-shadow: 0 0 0px 1000px $bg inset !important;
        -webkit-text-fill-color: $cursor !important;
      }
    }

  }

  .el-form-item {
    border: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    color: #454545;
  }
}
.el-input__wrapper {
    background: transparent !important;
    border: 0px !important;
    box-shadow: none !important;
}
</style>
<style scoped>
.login-container .el-input /deep/ input:-webkit-autofill {
  /* 自动填充文字颜色 */
  /* -webkit-text-fill-color: #ffe1b9 !important; */
  box-shadow: 0 0 0px 1000px rgba(255,255,255,0) inset !important;
  transition: background-color 5000s ease-in-out 0s;
}
</style>
<style lang="scss" scoped>
$bg:#ffffff;
$dark_gray:#fff;
$light_gray:#fff;
html, body, template{
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
.login-container {
  min-height: 100%;
  width: 100%;
  height: 100%;
  background: url('../../assets/customer_images/nokia-bg-img.png')  no-repeat center center fixed;
  // background-image: url('../../assets/customer_images/nokia-bg-img.png'), 
  //                   url('../../assets/customer_images/nokia-N-white.png');
  background-repeat: no-repeat, no-repeat; //没有覆盖到的区域不会被图片重叠来填充
  background-position: 100% 100%, 30% 50%;
  background-size: 100% 100%,100% 110%;
  overflow: hidden;
  
  .login-left{
    width: 55%;
    height: 100%;
    float: left;
    background: url('../../assets/customer_images/nokia-N-white.png') no-repeat;
    background-size:120% 107.5%; 
    background-position: 20% 0%;
    img{
      width: 100%;
      height: 100%;
      background: url('../../assets/customer_images/nokia_logo.png') no-repeat center center fixed;
      background-size:100% 10%; 
      // /*兼容浏览器版本*/
      -webkit-background-size: 10% 100%; 
      -o-background-size: cover;                
      background-size: cover;
    }
    
  }
  .login-right{
    width: 40%;
    height: 100%;
    float: right;

    .login-form-top{
      height: 15%;
      width: 100%;
      text-align: center;
      margin-top: 100px;
    }
    .login-form-bottom{
      height: 35%;
    }
    .login-form {
      // position: relative;
      // top: 10%;
      height: 50%;
      width: 400px;
      max-width: 100%;
      min-width: 300px;
      min-height: 400px;
      padding: 50px 35px 0;
      margin: 0 auto;
      overflow: hidden;
    }

  .tips {
    font-size: 14px;
      color: #f47f31;
    margin-bottom: 10px;

    span {
      &:first-of-type {
        margin-right: 16px;
      }
    }
  }

  .svg-container {
    padding: 6px 5px 6px 15px;
    color: $dark_gray;
    vertical-align: middle;
    width: 30px;
    display: inline-block;
  }

  .title-container {
    position: relative;

    .title {
      font-size: 26px;
      // color: $light_gray;

      color: #005aff;
      margin: 0px auto 40px auto;
      text-align: center;
      font-weight: bold;
    }
  }

  .show-pwd {
    position: absolute;
    right: 10px;
    top: 7px;
    font-size: 16px;
    color: $dark_gray;
    cursor: pointer;
    user-select: none;
  }
}
  
}

.el-input input::-ms-input-placeholder{
  color:    red;
}
</style>
