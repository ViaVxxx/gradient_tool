<template>
  <div class="relative">
    <!-- 渐变条背景 -->
    <div
      class="relative h-16 rounded-xl border-2 border-gray-300 dark:border-gray-600 overflow-hidden cursor-crosshair shadow-inner"
      :style="previewStyle"
      @click="addColorStopAtPosition">

      <!-- 网格线 -->
      <div class="absolute inset-0 opacity-20 pointer-events-none">
        <div v-for="i in 4" :key="i"
             class="absolute top-0 bottom-0 w-px bg-white"
             :style="{ left: (i * 25) + '%' }"></div>
      </div>

      <!-- 色标指示器 -->
      <div
        v-for="(stop, index) in colorStops"
        :key="index"
        class="absolute top-0 bottom-0 transform -translate-x-1/2 z-10 h-full pointer-events-none"
        :style="{ left: (stop.position * 100) + '%' }">

        <!-- 拖拽热区 (仅柱子) -->
        <div 
          class="absolute inset-y-0 left-1/2 -translate-x-1/2 w-6 flex justify-center items-center cursor-ew-resize pointer-events-auto touch-none group/drag"
          @mousedown.stop.prevent="startDragColorStop(index, $event)"
          @touchstart.stop.prevent="startDragColorStop(index, $event)">
          <!-- 可视化连接线 -->
          <div class="w-1 h-full bg-white/60 shadow-sm transition-all duration-200 group-hover/drag:bg-white group-hover/drag:w-1.5 group-active/drag:bg-indigo-200 group-active/drag:w-1.5 rounded-full"></div>
        </div>

        <!-- 色标手柄 (仅点击) -->
        <div
          class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-auto group/circle"
          @click.stop="selectColorStop(index)"
          @mousedown.stop> <!-- 阻止 mousedown 冒泡以防止触发拖拽 -->
          
          <div
            :class="[
              'w-6 h-6 rounded-full border-2 shadow-md transition-all duration-200 ring-2 ring-offset-2 ring-offset-gray-100 dark:ring-offset-gray-800',
              selectedColorStopIndex === index
                ? 'border-indigo-500 ring-indigo-400/80 scale-110 shadow-indigo-500/40'
                : 'border-white ring-transparent hover:scale-110 hover:ring-white/50'
            ]"
            :style="{ backgroundColor: stop.hex }">
          </div>

          <!-- 位置标签 (悬停显示) -->
          <div class="absolute -bottom-8 left-1/2 transform -translate-x-1/2 opacity-0 group-hover/circle:opacity-100 transition-opacity pointer-events-none z-20">
            <span class="text-[10px] bg-gray-900/90 text-white px-1.5 py-0.5 rounded shadow-sm whitespace-nowrap font-mono">
              {{ Math.round(stop.position * 100) }}%
            </span>
          </div>

          <!-- 删除按钮 -->
          <button
            v-if="colorStops.length > 2"
            @click.stop="removeColorStop(index)"
            class="absolute -top-2 -right-2 w-4 h-4 bg-red-500 text-white rounded-full text-[10px] opacity-0 group-hover/circle:opacity-100 transition-opacity flex items-center justify-center hover:bg-red-600 shadow-sm z-30">
            ×
          </button>
        </div>
      </div>
    </div>

    <!-- 位置标尺 -->
    <div class="flex justify-between text-xs text-gray-400 mt-2 px-4">
      <span>0%</span>
      <span>25%</span>
      <span>50%</span>
      <span>75%</span>
      <span>100%</span>
    </div>

    <!-- 色标详情 Pop-up -->
    <ColorStopPopover
      v-if="selectedColorStopIndex !== null"
      :stop="colorStops[selectedColorStopIndex]"
      :index="selectedColorStopIndex"
      @close="selectedColorStopIndex = null"
      @update="updateColorStop"
      @delete="removeColorStop(selectedColorStopIndex)" />
  </div>
</template>

<script setup>
import { useGradient } from '@/composables/useGradient'
import ColorStopPopover from './ColorStopPopover.vue'

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

function updateColorStop(index, updates) {
  Object.assign(colorStops.value[index], updates)
}
</script>
