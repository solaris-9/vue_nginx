<template>
  <section class="app-main">
    <router-view  v-slot="{ Component }" style="height: 100%;">
      <transition name="fade-transform" mode="out-in" style="height: 100%;">
        <keep-alive  style="height: 100%;">
          <component :is="Component" />
        </keep-alive>
      </transition>
    </router-view>
  </section>
</template>
<!-- <template>
  <section class="app-main">
    <transition name="fade-transform" mode="out-in" style="height: 100%;">
      <keep-alive  style="height: 100%;">
        <router-view  style="height: 100%;"></router-view>
      </keep-alive>
    </transition>
  </section>
</template> -->
<script>
export default {
  name: 'AppMain',
  computed: {
    key() {
      return this.$route.path
    },
    cachedViews () { 
      return this.$store.state.tagsView.cachedViews
    }
  }
}
</script>

<style scoped>
html, body, template {
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
}
.app-main {
  /*50 = navbar  */
  /* min-height: calc(100vh - 50px); */
  min-height: calc(100vh);
  width: 100%;
  height:  100%;
  position: relative;
  overflow: hidden;
  background-color: #f8f9fe;
  /* padding: 20px; */
}
.fixed-header+.app-main {
  padding-top: 70px;
}
</style>

<style lang="scss">
// fix css style bug in open el-dialog
.el-popup-parent--hidden {
  .fixed-header {
    padding-right: 15px;
  }
}
</style>
