<template>
  <section class="app-main">
    <router-view v-slot="{ Component, route }">
      <!-- <p>route = {{ route.fullPath }}</p> -->
      <transition name="fade-transform" mode="out-in">
        <keep-alive :include="cachedViews">
          <div :key="route.fullPath">
          <component :is="Component" />
          </div>
        </keep-alive>
      </transition>
    </router-view>
  </section>
</template>

<script setup >
import { computed } from 'vue';
import useStore from '@/store';

const { tagsView } = useStore();

const cachedViews = computed(() => tagsView.cachedViews);
</script>

<style lang="scss" scoped>
.app-main {
  /*50 = navbar  */
  min-height: calc(100vh - 50px);
  width: 100%;
  position: relative;
  overflow: hidden;
}
.fixed-header + .app-main {
  padding-top: 50px;
}

.hasTagsView {
  .app-main {
    /* 84 = navbar + tags-view = 50 + 34 */
    min-height: calc(100vh - 30px);
  }

  .fixed-header + .app-main {
    padding-top: 84px;
  }
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
