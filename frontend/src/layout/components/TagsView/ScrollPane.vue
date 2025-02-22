<template>
  <el-scrollbar
    ref="scrollContainer"
    :vertical="false"
    class="scroll-container"
    @wheel.prevent="handleScroll"
  >
    <slot></slot>
  </el-scrollbar>
</template>

<script setup >
import {
  ref,
  computed,
  onMounted,
  onBeforeUnmount,
  getCurrentInstance
} from 'vue';
import useStore from '@/store';

const tagAndTagSpacing = ref(4);
const { proxy } = getCurrentInstance();

const emits = defineEmits(['scroll']);
const emitScroll = () => {
  emits('scroll');
};

const { tagsView } = useStore();

const visitedViews = computed(() => tagsView.visitedViews);

const scrollWrapper = computed(
  () => proxy?.$refs.scrollContainer.$refs.wrapRef
);

onMounted(() => {
  scrollWrapper.value.addEventListener('scroll', emitScroll, true);
});
onBeforeUnmount(() => {
  scrollWrapper.value.removeEventListener('scroll', emitScroll);
});

function handleScroll(e) {
  const eventDelta = e.wheelDelta || -e.deltaY * 40;
  scrollWrapper.value.scrollLeft =
    scrollWrapper.value.scrollLeft + eventDelta / 4;
}

function moveToTarget(currentTag) {
  const $container = proxy.$refs.scrollContainer.$el;
  const $containerWidth = $container.offsetWidth;
  const $scrollWrapper = scrollWrapper.value;

  let firstTag = null;
  let lastTag = null;

  // find first tag and last tag
  if (visitedViews.value.length > 0) {
    firstTag = visitedViews.value[0];
    lastTag = visitedViews.value[visitedViews.value.length - 1];
  }

  if (firstTag === currentTag) {
    $scrollWrapper.scrollLeft = 0;
  } else if (lastTag === currentTag) {
    $scrollWrapper.scrollLeft = $scrollWrapper.scrollWidth - $containerWidth;
  } else {
    const tagListDom = document.getElementsByClassName('tags-view__item');
    const currentIndex = visitedViews.value.findIndex(
      item => item === currentTag
    );
    let prevTag = null;
    let nextTag = null;
    for (const k in tagListDom) {
      if (k !== 'length' && Object.hasOwnProperty.call(tagListDom, k)) {
        if (
          (tagListDom[k]).dataset.path ===
          visitedViews.value[currentIndex - 1].path
        ) {
          prevTag = tagListDom[k];
        }
        if (
          (tagListDom[k] ).dataset.path ===
          visitedViews.value[currentIndex + 1].path
        ) {
          nextTag = tagListDom[k];
        }
      }
    }

    // the tag's offsetLeft after of nextTag
    const afterNextTagOffsetLeft =
    nextTag.offsetLeft +
    nextTag.offsetWidth +
      tagAndTagSpacing.value;

    // the tag's offsetLeft before of prevTag
    const beforePrevTagOffsetLeft =
    prevTag.offsetLeft - tagAndTagSpacing.value;
    if (afterNextTagOffsetLeft > $scrollWrapper.scrollLeft + $containerWidth) {
      $scrollWrapper.scrollLeft = afterNextTagOffsetLeft - $containerWidth;
    } else if (beforePrevTagOffsetLeft < $scrollWrapper.scrollLeft) {
      $scrollWrapper.scrollLeft = beforePrevTagOffsetLeft;
    }
  }
}

defineExpose({
  moveToTarget
});
</script>

<style lang="scss" scoped>
.scroll-container {
  .el-scrollbar__bar {
    bottom: 0px;
  }

  .el-scrollbar__wrap {
    height: 49px;
  }
}

.scroll-container {
  white-space: nowrap;
  position: relative;
  overflow: hidden;
  width: 100%;
}
</style>
