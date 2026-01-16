<template>
  <div class="control-panel-container space-y-4">
    <!-- 渐变类型分段控制器 -->
    <div class="space-y-2">
      <label class="block text-xs font-medium text-gray-600 dark:text-gray-400">渐变类型</label>
      <div class="segmented-control inline-flex p-1 bg-gray-100 dark:bg-gray-800 rounded-lg w-full">
        <button
          v-for="type in gradientTypes"
          :key="type.value"
          @click="$emit('update:type', type.value)"
          :class="[
            'flex-1 px-4 py-2 text-sm font-medium rounded-md transition-all duration-200',
            modelType === type.value
              ? 'bg-white dark:bg-gray-700 text-indigo-600 dark:text-indigo-400 shadow-sm'
              : 'text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-gray-200'
          ]">
          {{ type.label }}
        </button>
      </div>
    </div>

    <!-- 角度控制器 (仅线性渐变) -->
    <div v-if="modelType === 'linear'" class="space-y-3">
      <label class="block text-xs font-medium text-gray-600 dark:text-gray-400">角度</label>

      <div class="flex items-center gap-4">
        <!-- 角度拨盘 -->
        <div class="relative">
          <svg
            ref="angleDial"
            class="w-16 h-16 cursor-pointer"
            viewBox="0 0 64 64"
            @mousedown="startAngleDrag"
            @touchstart="startAngleDrag">
            <!-- 背景圆 -->
            <circle
              cx="32"
              cy="32"
              r="28"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              class="text-gray-200 dark:text-gray-700" />

            <!-- 刻度线 -->
            <g v-for="i in 12" :key="i" class="text-gray-300 dark:text-gray-600">
              <line
                :x1="32 + 24 * Math.cos((i * 30 - 90) * Math.PI / 180)"
                :y1="32 + 24 * Math.sin((i * 30 - 90) * Math.PI / 180)"
                :x2="32 + 28 * Math.cos((i * 30 - 90) * Math.PI / 180)"
                :y2="32 + 28 * Math.sin((i * 30 - 90) * Math.PI / 180)"
                stroke="currentColor"
                stroke-width="1" />
            </g>

            <!-- 指示线 -->
            <line
              :x1="32"
              :y1="32"
              :x2="32 + 20 * Math.cos((modelAngle - 90) * Math.PI / 180)"
              :y2="32 + 20 * Math.sin((modelAngle - 90) * Math.PI / 180)"
              stroke="currentColor"
              stroke-width="3"
              stroke-linecap="round"
              class="text-indigo-500" />

            <!-- 中心点 -->
            <circle
              cx="32"
              cy="32"
              r="4"
              fill="currentColor"
              class="text-indigo-500" />
          </svg>

          <!-- 角度标签 -->
          <div class="absolute -bottom-1 left-1/2 -translate-x-1/2 text-[10px] font-mono text-gray-500">
            {{ modelAngle }}°
          </div>
        </div>

        <!-- 数字输入框 -->
        <div class="flex-1">
          <div class="relative">
            <input
              type="number"
              :value="modelAngle"
              @input="handleAngleInput"
              @keydown.up.prevent="adjustAngle(1)"
              @keydown.down.prevent="adjustAngle(-1)"
              min="0"
              max="360"
              class="w-full px-3 py-2 pr-8 text-center text-lg font-bold text-indigo-600 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <span class="absolute right-3 top-1/2 -translate-y-1/2 text-sm text-gray-400 pointer-events-none">°</span>
          </div>

          <!-- 角度滑块 -->
          <input
            type="range"
            :value="modelAngle"
            @input="handleAngleInput"
            min="0"
            max="360"
            class="w-full h-2 mt-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider">
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  modelType: {
    type: String,
    default: 'linear'
  },
  modelAngle: {
    type: Number,
    default: 90
  }
})

const emit = defineEmits(['update:type', 'update:angle'])

const gradientTypes = [
  { label: 'Linear', value: 'linear' },
  { label: 'Radial', value: 'radial' }
]

const angleDial = ref(null)

function handleAngleInput(event) {
  let value = parseInt(event.target.value)
  if (isNaN(value)) return

  value = ((value % 360) + 360) % 360 // 确保在 0-360 范围内
  emit('update:angle', value)
}

function adjustAngle(delta) {
  let newAngle = props.modelAngle + delta
  newAngle = ((newAngle % 360) + 360) % 360
  emit('update:angle', newAngle)
}

function startAngleDrag(event) {
  event.preventDefault()

  const svg = angleDial.value
  const rect = svg.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2

  const updateAngle = (clientX, clientY) => {
    const dx = clientX - centerX
    const dy = clientY - centerY
    let angle = Math.atan2(dy, dx) * 180 / Math.PI + 90

    // 确保角度在 0-360 范围内
    angle = ((angle % 360) + 360) % 360
    emit('update:angle', Math.round(angle))
  }

  const handleMove = (e) => {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    const clientY = e.touches ? e.touches[0].clientY : e.clientY
    updateAngle(clientX, clientY)
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
  updateAngle(clientX, clientY)

  document.addEventListener('mousemove', handleMove)
  document.addEventListener('mouseup', handleEnd)
  document.addEventListener('touchmove', handleMove)
  document.addEventListener('touchend', handleEnd)
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

/* 滑块样式 */
.slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #6366f1;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #6366f1;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
</style>
