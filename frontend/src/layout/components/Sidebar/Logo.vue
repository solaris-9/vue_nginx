<template>
  <div class="sidebar-logo-container" :class="{'collapse':collapse}">
    <transition name="sidebarLogoFade">
      <router-link v-if="collapse" key="collapse" class="sidebar-logo-link" to="/">
        <img class="sidebar-logo" src="@/assets/customer_images/nokia-logo-black.png"/>
        <!-- <img v-if="logo" :src="logo" class="sidebar-logo"> -->
        <!-- <h1 v-else class="sidebar-title">{{ title }} </h1> -->
      </router-link>
      <router-link v-else key="expand" class="sidebar-logo-link" to="/">
          <img class="sidebar-logo" v-if="logo" :src=logo />
          <!-- <h1 class="sidebar-title"><i style="margin: 0 8px;color: #cecdcd;">|</i>{{ title }} </h1> -->
      </router-link>
    </transition>
  </div>
</template>

<script>
import "../../../assets/nokia-svg/nokia-logo-black.svg"
export default {
  name: 'SidebarLogo',
  props: {
    collapse: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      title: 'BBD Device Deployment',
      logo: require('@/assets/nokia-svg/nokia-logo-black.svg')
    }
  }
}
</script>

<style lang="scss" scoped>
.sidebarLogoFade-enter-active {
  transition: opacity 1.5s;
}

.sidebarLogoFade-enter,
.sidebarLogoFade-leave-to {
  opacity: 0;
}

.sidebar-logo-container {
  position: relative;
  width: 100%;
  height: 50px;
  line-height: 50px;
  background: #b0d2fa;
  text-align: center;
  overflow: hidden;

  & .sidebar-logo-link {
    height: 100%;
    width: 100%;

    & .sidebar-logo {
      width:  150px;
      height: 50px;
      vertical-align: middle;
    }

    & .sidebar-title {
      display: inline-block;
      margin: 0;
      color: #000000;
      font-weight: 800;
      line-height: 50px;
      font-size: 14px;
      font-family: Avenir, Helvetica Neue, Arial, Helvetica, sans-serif;
      vertical-align: middle;
    }
  }

  &.collapse {
    .sidebar-logo {
      margin: auto 0;
      width: 40px;
      height: 50px;
    }
  }
}
</style>
