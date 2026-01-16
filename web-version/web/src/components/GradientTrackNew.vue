<template>
  <div class="relative">
    <!-- 渐变条背景 -->
    <div
      class="relative h-6 rounded-xl border-2 border-gray-300 dark:border-gray-600 overflow-visible cursor-crosshair shadow-inner"
      :style="previewStyle"
      @click="addColorStopAtPosition">

      <!-- 网格线 -->
      <div class="absolute inset-0 opacity-20 pointer-events-none overflow-hidden rounded-xl">
        <div v-for="i in 4" :key="i"
             class="absolute top-0 bottom-0 w-px bg-white"
             :style="{ left: (i * 25) + '%' }"></div>
      </div>

      <!-- 色标手柄组件 -->
      <GradientHandle
        v-for="(stop, index) in colorStops"
        :key="index"
        :stop="stop"
        :is-selected="selectedColorStopIndex === index"
        :can-delete="colorStops.length > 2"
        @select="selectColorStop(index)"
        @delete="removeColorStop(index)"
        @start-drag="startDragColorStop(index, $event)"
        @update-position="updateStopPosition(index, $event)" />
    </div>

    <!-- 位置标尺 -->
    <div class="flex justify-between text-xs text-gray-400 mt-2 px-4">
      <span>0%</span>
      <span>25%</span>
      <span>50%</span>
      <span>75%</span>
      <span>100%</span>
    </div>
  </div>
</template>

<script setup>
import { useGradient } from '@/composables/useGradient'
import GradientHandle from './GradientHandle.vue'

const {
  colorStops,
  selectedColorStopIndex,
  previewStyle,
  isDragging,
  hexToRgb,
  rgbToHex,
  interpolateColorAtPosition
} = useGradient()

function selectColorStop(index) {
  selectedColorStopIndex.value = index
}

function addColorStopAtPosition(event) {
  if (colorStops.value.length >= 20) return

  const rect = event.currentTarget.getBoundingClientRect()
  const x = event.clientX - rect.left
  const position = Math.max(0, Math.min(1, x / rect.width))

  const interpolatedColor = interpolateColorAtPosition(colorStops.value, position)

  const newStop = {
    position: Math.round(position * 100) / 100,
    color: interpolatedColor,
    hex: rgbToHex(interpolatedColor.r, interpolatedColor.g, interpolatedColor.b),
    alpha: 100
  }

  let insertIndex = colorStops.value.findIndex(stop => stop.position > position)
  if (insertIndex === -1) insertIndex = colorStops.value.length

  colorStops.value.splice(insertIndex, 0, newStop)
  selectedColorStopIndex.value = insertIndex
}

function startDragColorStop(index, event) {
  event.preventDefault()
  selectedColorStopIndex.value = index
  isDragging.value = true

  // 拖拽时禁用 backdrop-filter 以提升性能
  const sidebar = document.querySelector('aside')
  if (sidebar) {
    sidebar.classList.add('disable-blur')
  }

  const gradientBar = event.currentTarget.closest('.relative')
  const rect = gradientBar.getBoundingClientRect()

  let rafId = null

  const updatePosition = (clientX) => {
    const x = clientX - rect.left
    const position = Math.max(0, Math.min(1, x / rect.width))
    colorStops.value[index].position = Math.round(position * 100) / 100
  }

  const handleMove = (e) => {
    if (rafId) return
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    rafId = requestAnimationFrame(() => {
      updatePosition(clientX)
      rafId = null
    })
  }

  const handleEnd = () => {
    if (rafId) {
      cancelAnimationFrame(rafId)
      rafId = null
    }
    isDragging.value = false

    // 恢复 backdrop-filter
    if (sidebar) {
      sidebar.classList.remove('disable-blur')
    }

    document.removeEventListener('mousemove', handleMove)
    document.removeEventListener('mouseup', handleEnd)
    document.removeEventListener('touchmove', handleMove)
    document.removeEventListener('touchend', handleEnd)
  }

  document.addEventListener('mousemove', handleMove)
  document.addEventListener('mouseup', handleEnd)
  document.addEventListener('touchmove', handleMove)
  document.addEventListener('touchend', handleEnd)
}

function removeColorStop(index) {
  if (colorStops.value.length <= 2) return

  colorStops.value.splice(index, 1)

  if (selectedColorStopIndex.value >= colorStops.value.length) {
    selectedColorStopIndex.value = colorStops.value.length - 1
  } else if (selectedColorStopIndex.value === index && index > 0) {
    selectedColorStopIndex.value = index - 1
  }
}

function updateStopPosition(index, position) {
  colorStops.value[index].position = Math.round(position * 100) / 100
}
</script>
