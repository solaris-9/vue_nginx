<template>
  <div class="login-container">
    <div class="login-left"></div>
    <div class="login-right">
      <div class="login-form-top"></div>
      
      <LoginForm />

      <div class="login-form-bottom">
        <p style="text-align: center; margin-top: 50px; color: #ffffff;">
          @Copy right Nokia 2024
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import LoginForm from "./LoginForm.vue";
</script>

<style lang="scss">
.login-container {
  display: flex;
  height: 100vh;
  background: url("@/assets/customer_images/nokia-bg-img.png") no-repeat center center fixed;
  background-size: cover;

  .login-left {
    width: 55%;
    background: url("@/assets/customer_images/nokia-N-white.png") no-repeat;
    background-size: 120% 107.5%;
    background-position: 20% 0%;
  }

  .login-right {
    width: 45%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
  }
}
</style>
