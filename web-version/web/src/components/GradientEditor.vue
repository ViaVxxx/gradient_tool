<template>
  <div class="gradient-editor flex flex-col gap-6 p-6">
    <!-- 顶部：渐变条 -->
    <section class="gradient-track-section">
      <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3 flex items-center">
        <svg class="w-4 h-4 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
        </svg>
        渐变预览
      </h3>
      <GradientTrackNew />
    </section>

    <!-- 中部：控制面板 -->
    <section class="control-section">
      <ControlPanel
        :model-type="gradientType"
        :model-angle="angle"
        @update:type="gradientType = $event"
        @update:angle="angle = $event" />
    </section>

    <!-- 底部：双栏布局 (列表 + 拾色器) -->
    <section class="editor-panel grid grid-cols-1 lg:grid-cols-[1fr_300px] gap-6">
      <!-- 左侧：色标列表 -->
      <div class="stops-section">
        <StopsList
          :stops="colorStops"
          :selected-index="selectedColorStopIndex"
          @select="selectStop"
          @update:stop="updateStop"
          @delete="deleteStop"
          @add="addStop" />
      </div>

      <!-- 右侧：拾色器 -->
      <div class="picker-section">
        <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">颜色编辑器</h4>
        <ColorPicker
          v-if="selectedColorStopIndex !== null"
          :color="colorStops[selectedColorStopIndex].color"
          :alpha="colorStops[selectedColorStopIndex].alpha"
          @update:color="updateStopColor"
          @update:alpha="updateStopAlpha" />
        <div v-else class="flex items-center justify-center h-64 text-sm text-gray-400">
          请选择一个色标进行编辑
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useGradient } from '@/composables/useGradient'
import GradientTrackNew from './GradientTrackNew.vue'
import StopsList from './StopsList.vue'
import ColorPicker from './ColorPicker.vue'
import ControlPanel from './ControlPanel.vue'

const {
  gradientType,
  angle,
  colorStops,
  selectedColorStopIndex,
  rgbToHex,
  hexToRgb,
  interpolateColorAtPosition
} = useGradient()

function selectStop(index) {
  selectedColorStopIndex.value = index
}

function updateStop(index, updates) {
  // 更新色标数据
  if (updates.hex !== undefined) {
    const rgb = hexToRgb(updates.hex)
    if (rgb) {
      colorStops.value[index].color = rgb
      colorStops.value[index].hex = updates.hex
    }
  }

  if (updates.position !== undefined) {
    colorStops.value[index].position = updates.position
  }
}

function deleteStop(index) {
  if (colorStops.value.length <= 2) return

  colorStops.value.splice(index, 1)

  // 调整选中索引
  if (selectedColorStopIndex.value >= colorStops.value.length) {
    selectedColorStopIndex.value = colorStops.value.length - 1
  } else if (selectedColorStopIndex.value === index && index > 0) {
    selectedColorStopIndex.value = index - 1
  }
}

function addStop() {
  if (colorStops.value.length >= 20) return

  // 在中间位置添加新色标
  const newPosition = 0.5
  const interpolatedColor = interpolateColorAtPosition(colorStops.value, newPosition)

  const newStop = {
    position: newPosition,
    color: interpolatedColor,
    hex: rgbToHex(interpolatedColor.r, interpolatedColor.g, interpolatedColor.b),
    alpha: 100
  }

  // 找到插入位置
  let insertIndex = colorStops.value.findIndex(stop => stop.position > newPosition)
  if (insertIndex === -1) insertIndex = colorStops.value.length

  colorStops.value.splice(insertIndex, 0, newStop)
  selectedColorStopIndex.value = insertIndex
}

function updateStopColor(rgb) {
  if (selectedColorStopIndex.value === null) return

  colorStops.value[selectedColorStopIndex.value].color = rgb
  colorStops.value[selectedColorStopIndex.value].hex = rgbToHex(rgb.r, rgb.g, rgb.b)
}

function updateStopAlpha(alpha) {
  if (selectedColorStopIndex.value === null) return

  colorStops.value[selectedColorStopIndex.value].alpha = alpha
}
</script>

<style scoped>
/* 响应式适配 */
@media (max-width: 1023px) {
  .editor-panel {
    grid-template-columns: 1fr;
  }
}
</style>
