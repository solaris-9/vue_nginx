<template>
        <el-form
          ref="loginFormRef"
          :model="form"
          :rules="loginRules"
          class="login-form"
          auto-complete="on"
          label-position="left"
        >
          <div class="title-container">
            <img
              class="title"
              src="@/assets/customer_images/nokia_logo.png"
              alt="Nokia Logo"
              style="height: 30px; width: 120px;"
            />
          </div>
          
          <el-form-item prop="username" style="background-color: transparent;">
            <el-input
              v-model="form.username"
              placeholder="Username"
              size="large"
              tabindex="1"
              autocomplete="off"
              :prefix-icon="User"
            />
          </el-form-item>
          
          <el-form-item prop="password" style="background-color: transparent;">
            <el-input
              ref="passwordRef"
              v-model="form.password"
              type="password"
              placeholder="Password"
              size="large"
              tabindex="2"
              @keyup.enter="handleLogin"
              :prefix-icon="Lock"
              show-password
            />
          </el-form-item>
          
          <el-button
            :loading="loading"
            type="primary"
            class="login-button"
            @click.prevent="handleLogin"
          >
            Login Device Deployment Tool
          </el-button>
          
          <div class="tips"></div>
        </el-form>
  </template>
  
  <script setup lang="ts">
  import { ref, reactive, watch } from "vue";
  import { useRouter, useRoute } from "vue-router";
  import { ElForm, ElMessage } from "element-plus";
  import { validUsername } from "@/utils/validate";
  import { Lock, User } from '@element-plus/icons-vue'
  import useStore from "@/store";
  
  const { user } = useStore();
  const router = useRouter();
  const route = useRoute();
  
  // Reactive data
  const form = reactive({
    username: "",
    password: "",
  });
  
  const loginRules = {
    username: [
      {
        required: true,
        trigger: "blur",
        validator: (rule: any, value: string, callback: Function) => {
          if (!validUsername(value)) {
            callback(new Error("Please enter the correct user name"));
          } else {
            callback();
          }
        },
      },
    ],
    password: [
      {
        required: true,
        trigger: "blur",
        validator: (rule: any, value: string, callback: Function) => {
          if (value.length < 6) {
            callback(new Error("The password cannot be less than 6 characters"));
          } else {
            callback();
          }
        },
      },
    ],
  };
  
  const passwordType = ref("password");
  const loading = ref(false);
  const loginFormRef = ref<InstanceType<typeof ElForm>>();
  const passwordRef = ref<HTMLElement>();
  let redirect = route.query?.redirect as string;
  
  // Watch for route changes
  watch(route, (newRoute) => {
    redirect = newRoute.query?.redirect as string;
  });
  
  // Handle login
  const handleLogin = () => {
    loginFormRef.value?.validate((valid: boolean) => {
      if (valid) {
        loading.value = true;
        user
          .login(form)
          .then(() => {
            console.log("Login successfull")
            return user.getUserInfo();
          })
          .then(() => {
            router.push({ path: redirect || "/" });
            loading.value = false;
          })
          .catch(() => {
            loading.value = false;
          });
      } else {
        ElMessage.error("Login failed. Please check your input.");
      }
    });
  };
  </script>
  
  <style lang="scss">
      .login-form {
        width: 400px;
        max-width: 100%;
        padding: 50px 35px;
        border-radius: 8px;
      
        .el-input__wrapper {
          background-color: transparent;
          box-shadow: none;
        
          .el-input__prefix {
            color: white;
          }
          .el-input__inner {
            color: white;
          }
        }

        .el-form-item {
          margin-bottom: 30px;
        }
      }
  
      .title-container {
        margin-bottom: 40px;
  
        .title {
          display: block;
          margin: 0 auto;
          font-size: 26px;
          color: #005aff;
          font-weight: bold;
        }
      }
  
      .login-button {
        width: 100%;
        margin-top: 30px;
        background: linear-gradient(to bottom right, #005aff, rgb(134, 22, 83));
      }
  
      .tips {
        font-size: 14px;
        color: #f47f31;
        text-align: center;
        margin-top: 10px;
      }
  </style>
  