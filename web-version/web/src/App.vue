<template>
  <div class="h-screen w-screen flex overflow-hidden bg-gray-50 dark:bg-gray-900">

    <!-- 侧边栏 -->
    <Sidebar
      ref="sidebarRef"
      @open-presets="showPresetDrawer = true" />

    <!-- 预览区 -->
    <Preview @toggle-sidebar="toggleSidebar" />

    <!-- 预设抽屉 -->
    <PresetDrawer
      :is-open="showPresetDrawer"
      @close="showPresetDrawer = false" />

    <!-- 移动端遮罩层 -->
    <div
      v-if="isMobile && isSidebarOpen"
      @click="toggleSidebar"
      class="lg:hidden fixed inset-0 bg-black/50 backdrop-blur-sm z-20">
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useGradient } from '@/composables/useGradient'
import Sidebar from '@/components/Sidebar.vue'
import Preview from '@/components/Preview.vue'
import PresetDrawer from '@/components/PresetDrawer.vue'

const { waitForAPI, loadPresets, generateGradient } = useGradient()

const showPresetDrawer = ref(false)
const sidebarRef = ref(null)
const windowWidth = ref(window.innerWidth)

const isMobile = computed(() => windowWidth.value < 1024)
const isSidebarOpen = ref(false)

function toggleSidebar() {
  if (sidebarRef.value) {
    sidebarRef.value.toggleSidebar()
    isSidebarOpen.value = !isSidebarOpen.value
  }
}

// 监听窗口大小变化
function handleResize() {
  windowWidth.value = window.innerWidth
}

// 初始化
onMounted(async () => {
  window.addEventListener('resize', handleResize)
  await waitForAPI()
  await loadPresets()
  await generateGradient()
})
</script>
