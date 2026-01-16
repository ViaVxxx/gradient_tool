<template>
  <div class="color-picker-container space-y-4">
    <!-- 主色域选择器 (256x256) -->
    <div class="relative">
      <div
        ref="saturationArea"
        class="w-64 h-64 rounded-lg cursor-crosshair relative overflow-hidden shadow-inner border-2 border-gray-200 dark:border-gray-600"
        :style="saturationAreaStyle"
        @mousedown="startSaturationDrag"
        @touchstart="startSaturationDrag">

        <!-- 白色到透明渐变 (饱和度) -->
        <div class="absolute inset-0 bg-gradient-to-r from-white to-transparent"></div>

        <!-- 透明到黑色渐变 (亮度) -->
        <div class="absolute inset-0 bg-gradient-to-t from-black to-transparent"></div>

        <!-- 选择器指示器 -->
        <div
          class="absolute w-4 h-4 border-2 border-white rounded-full shadow-lg pointer-events-none transform -translate-x-1/2 -translate-y-1/2"
          :style="{ left: saturation * 100 + '%', top: (1 - value) * 100 + '%' }">
          <div class="w-full h-full rounded-full ring-1 ring-black/20"></div>
        </div>
      </div>
    </div>

    <!-- 色相滑块 -->
    <div class="space-y-2">
      <label class="block text-xs font-medium text-gray-600 dark:text-gray-400">色相</label>
      <div class="relative h-3 rounded-full overflow-hidden shadow-inner border border-gray-200 dark:border-gray-600 cursor-pointer"
           ref="hueSlider"
           @mousedown="startHueDrag"
           @touchstart="startHueDrag">
        <!-- 彩虹渐变 -->
        <div class="absolute inset-0 bg-gradient-to-r from-red-500 via-yellow-500 via-green-500 via-cyan-500 via-blue-500 via-purple-500 to-red-500"></div>

        <!-- 滑块指示器 -->
        <div
          class="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-white border-2 border-gray-300 rounded-full shadow-md pointer-events-none transform -translate-x-1/2"
          :style="{ left: (hue / 360) * 100 + '%' }">
        </div>
      </div>
    </div>

    <!-- 透明度滑块 -->
    <div class="space-y-2">
      <label class="block text-xs font-medium text-gray-600 dark:text-gray-400">透明度</label>
      <div class="relative h-3 rounded-full overflow-hidden shadow-inner border border-gray-200 dark:border-gray-600 cursor-pointer bg-checkerboard"
           ref="alphaSlider"
           @mousedown="startAlphaDrag"
           @touchstart="startAlphaDrag">
        <!-- 颜色渐变叠加 -->
        <div
          class="absolute inset-0"
          :style="{ background: `linear-gradient(to right, transparent, ${currentColorHex})` }">
        </div>

        <!-- 滑块指示器 -->
        <div
          class="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-white border-2 border-gray-300 rounded-full shadow-md pointer-events-none transform -translate-x-1/2"
          :style="{ left: alpha + '%' }">
        </div>
      </div>
    </div>

    <!-- 颜色输入组 -->
    <div class="space-y-3">
      <!-- HEX 输入 (长框) -->
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">HEX</label>
        <input
          type="text"
          :value="currentColorHex"
          @input="handleHexInput"
          class="w-full px-3 py-2 text-sm font-mono bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="#000000">
      </div>

      <!-- RGBA 输入 (四个短框) -->
      <div>
        <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">RGBA</label>
        <div class="grid grid-cols-4 gap-2">
          <div>
            <input
              type="number"
              :value="color.r"
              @input="handleRgbInput('r', $event)"
              min="0" max="255"
              class="w-full px-2 py-2 text-xs text-center font-mono bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500">
            <span class="block text-[10px] text-gray-400 text-center mt-1">R</span>
          </div>
          <div>
            <input
              type="number"
              :value="color.g"
              @input="handleRgbInput('g', $event)"
              min="0" max="255"
              class="w-full px-2 py-2 text-xs text-center font-mono bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500">
            <span class="block text-[10px] text-gray-400 text-center mt-1">G</span>
          </div>
          <div>
            <input
              type="number"
              :value="color.b"
              @input="handleRgbInput('b', $event)"
              min="0" max="255"
              class="w-full px-2 py-2 text-xs text-center font-mono bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500">
            <span class="block text-[10px] text-gray-400 text-center mt-1">B</span>
          </div>
          <div>
            <input
              type="number"
              :value="Math.round(alpha)"
              @input="handleAlphaInput"
              min="0" max="100"
              class="w-full px-2 py-2 text-xs text-center font-mono bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500">
            <span class="block text-[10px] text-gray-400 text-center mt-1">A</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  color: {
    type: Object,
    required: true,
    validator: (val) => val.r !== undefined && val.g !== undefined && val.b !== undefined
  },
  alpha: {
    type: Number,
    default: 100
  }
})

const emit = defineEmits(['update:color', 'update:alpha'])

// HSV 状态
const hue = ref(0)
const saturation = ref(1)
const value = ref(1)

// 引用
const saturationArea = ref(null)
const hueSlider = ref(null)
const alphaSlider = ref(null)

// 计算属性
const saturationAreaStyle = computed(() => ({
  backgroundColor: `hsl(${hue.value}, 100%, 50%)`
}))

const currentColorHex = computed(() => {
  return rgbToHex(props.color.r, props.color.g, props.color.b)
})

// 初始化：从 RGB 转换到 HSV
watch(() => props.color, (newColor) => {
  const hsv = rgbToHsv(newColor.r, newColor.g, newColor.b)
  hue.value = hsv.h
  saturation.value = hsv.s
  value.value = hsv.v
}, { immediate: true })

// 颜色转换函数
function rgbToHsv(r, g, b) {
  r /= 255
  g /= 255
  b /= 255

  const max = Math.max(r, g, b)
  const min = Math.min(r, g, b)
  const delta = max - min

  let h = 0
  const s = max === 0 ? 0 : delta / max
  const v = max

  if (delta !== 0) {
    if (max === r) {
      h = ((g - b) / delta + (g < b ? 6 : 0)) / 6
    } else if (max === g) {
      h = ((b - r) / delta + 2) / 6
    } else {
      h = ((r - g) / delta + 4) / 6
    }
  }

  return { h: h * 360, s, v }
}

function hsvToRgb(h, s, v) {
  h = h / 360
  const i = Math.floor(h * 6)
  const f = h * 6 - i
  const p = v * (1 - s)
  const q = v * (1 - f * s)
  const t = v * (1 - (1 - f) * s)

  let r, g, b
  switch (i % 6) {
    case 0: r = v; g = t; b = p; break
    case 1: r = q; g = v; b = p; break
    case 2: r = p; g = v; b = t; break
    case 3: r = p; g = q; b = v; break
    case 4: r = t; g = p; b = v; break
    case 5: r = v; g = p; b = q; break
  }

  return {
    r: Math.round(r * 255),
    g: Math.round(g * 255),
    b: Math.round(b * 255)
  }
}

function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map(x => {
    const hex = x.toString(16)
    return hex.length === 1 ? '0' + hex : hex
  }).join('')
}

function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null
}

// 饱和度/亮度选择器拖拽
function startSaturationDrag(event) {
  event.preventDefault()
  const rect = saturationArea.value.getBoundingClientRect()

  const updateSV = (clientX, clientY) => {
    const x = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width))
    const y = Math.max(0, Math.min(1, (clientY - rect.top) / rect.height))

    saturation.value = x
    value.value = 1 - y

    const rgb = hsvToRgb(hue.value, saturation.value, value.value)
    emit('update:color', rgb)
  }

  const handleMove = (e) => {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    const clientY = e.touches ? e.touches[0].clientY : e.clientY
    updateSV(clientX, clientY)
  }

  const handleEnd = () => {
    document.removeEventListener('mousemove', handleMove)
    document.removeEventListener('mouseup', handleEnd)
    document.removeEventListener('touchmove', handleMove)
    document.removeEventListener('touchend', handleEnd)
  }

  // 初始点击
  const clientX = event.touches ? event.touches[0].clientX : event.clientX
  const clientY = event.touches ? event.touches[0].clientY : event.clientY
  updateSV(clientX, clientY)

  document.addEventListener('mousemove', handleMove)
  document.addEventListener('mouseup', handleEnd)
  document.addEventListener('touchmove', handleMove)
  document.addEventListener('touchend', handleEnd)
}

// 色相滑块拖拽
function startHueDrag(event) {
  event.preventDefault()
  const rect = hueSlider.value.getBoundingClientRect()

  const updateHue = (clientX) => {
    const x = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width))
    hue.value = x * 360

    const rgb = hsvToRgb(hue.value, saturation.value, value.value)
    emit('update:color', rgb)
  }

  const handleMove = (e) => {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    updateHue(clientX)
  }

  const handleEnd = () => {
    document.removeEventListener('mousemove', handleMove)
    document.removeEventListener('mouseup', handleEnd)
    document.removeEventListener('touchmove', handleMove)
    document.removeEventListener('touchend', handleEnd)
  }

  const clientX = event.touches ? event.touches[0].clientX : event.clientX
  updateHue(clientX)

  document.addEventListener('mousemove', handleMove)
  document.addEventListener('mouseup', handleEnd)
  document.addEventListener('touchmove', handleMove)
  document.addEventListener('touchend', handleEnd)
}

// 透明度滑块拖拽
function startAlphaDrag(event) {
  event.preventDefault()
  const rect = alphaSlider.value.getBoundingClientRect()

  const updateAlpha = (clientX) => {
    const x = Math.max(0, Math.min(1, (clientX - rect.left) / rect.width))
    emit('update:alpha', Math.round(x * 100))
  }

  const handleMove = (e) => {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    updateAlpha(clientX)
  }

  const handleEnd = () => {
    document.removeEventListener('mousemove', handleMove)
    document.removeEventListener('mouseup', handleEnd)
    document.removeEventListener('touchmove', handleMove)
    document.removeEventListener('touchend', handleEnd)
  }

  const clientX = event.touches ? event.touches[0].clientX : event.clientX
  updateAlpha(clientX)

  document.addEventListener('mousemove', handleMove)
  document.addEventListener('mouseup', handleEnd)
  document.addEventListener('touchmove', handleMove)
  document.addEventListener('touchend', handleEnd)
}

// 输入处理
function handleHexInput(event) {
  let hex = event.target.value.trim()
  if (!hex.startsWith('#')) hex = '#' + hex

  const rgb = hexToRgb(hex)
  if (rgb) {
    emit('update:color', rgb)
  }
}

function handleRgbInput(channel, event) {
  let value = parseInt(event.target.value)
  if (isNaN(value)) return

  value = Math.max(0, Math.min(255, value))
  const newColor = { ...props.color, [channel]: value }
  emit('update:color', newColor)
}

function handleAlphaInput(event) {
  let value = parseInt(event.target.value)
  if (isNaN(value)) return

  value = Math.max(0, Math.min(100, value))
  emit('update:alpha', value)
}
</script>

<style scoped>
/* 隐藏数字输入框的上下箭头 */
input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}

input[type="number"] {
  -moz-appearance: textfield;
}
</style>
