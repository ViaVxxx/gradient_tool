<template>
  <div class="flex items-center justify-between gap-4 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
    <!-- Type Selector -->
    <div class="relative flex p-1 bg-gray-100 dark:bg-gray-700 rounded-lg">
      <!-- 滑块背景 -->
      <div
        class="absolute inset-y-1 bg-white dark:bg-gray-600 rounded-md shadow transition-transform duration-300 ease-out"
        :style="{
          width: '50%',
          transform: type === 'radial' ? 'translateX(100%)' : 'translateX(0)'
        }">
      </div>

      <!-- 按钮 -->
      <button
        v-for="t in ['linear', 'radial']"
        :key="t"
        class="relative z-10 px-4 py-1.5 text-sm font-medium rounded-md transition-colors capitalize"
        :class="type === t ? 'text-indigo-600 dark:text-indigo-400' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400'"
        @click="$emit('update:type', t)"
      >
        {{ t }}
      </button>
    </div>

    <!-- Angle Control (Visible only for Linear) -->
    <div
      v-if="type === 'linear'"
      class="flex items-center gap-4"
    >
      <!-- Dial (左侧，更大) -->
      <div
        class="relative w-12 h-12 cursor-pointer group flex-shrink-0"
        @mousedown="startAngleDrag"
      >
        <!-- 外圈 -->
        <svg class="w-full h-full text-gray-300 dark:text-gray-600 group-hover:text-indigo-400 transition-colors" viewBox="0 0 48 48">
          <circle cx="24" cy="24" r="22" fill="none" stroke="currentColor" stroke-width="2" />
          <!-- 刻度线 -->
          <line v-for="i in 12" :key="i"
            :x1="24 + 18 * Math.cos((i * 30 - 90) * Math.PI / 180)"
            :y1="24 + 18 * Math.sin((i * 30 - 90) * Math.PI / 180)"
            :x2="24 + 22 * Math.cos((i * 30 - 90) * Math.PI / 180)"
            :y2="24 + 22 * Math.sin((i * 30 - 90) * Math.PI / 180)"
            stroke="currentColor"
            stroke-width="1.5"
            opacity="0.5" />
        </svg>

        <!-- 指示箭头 -->
        <div
          class="absolute top-1/2 left-1/2 origin-left transform -translate-y-1/2 pointer-events-none transition-transform duration-150"
          :style="{ transform: `translate(-50%, -50%) rotate(${angle}deg)` }"
        >
          <svg class="w-5 h-5 text-indigo-500" viewBox="0 0 20 20" fill="currentColor">
            <path d="M10 2 L10 10 L14 8 Z" />
          </svg>
        </div>

        <!-- 中心点 -->
        <div class="absolute top-1/2 left-1/2 w-2 h-2 bg-indigo-500 rounded-full transform -translate-x-1/2 -translate-y-1/2"></div>
      </div>

      <!-- Number Input (右侧) -->
      <div class="relative">
        <input
          type="number"
          :value="angle"
          @input="onAngleInput"
          min="0"
          max="359"
          class="w-20 text-center px-3 py-2 text-sm font-medium border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-400 pointer-events-none">°</span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  type: String,
  angle: Number
})

const emit = defineEmits(['update:type', 'update:angle'])

function onAngleInput(e) {
  let val = parseInt(e.target.value)
  if (isNaN(val)) val = 0
  emit('update:angle', val % 360)
}

function startAngleDrag(e) {
  const rect = e.currentTarget.getBoundingClientRect()
  const centerX = rect.left + rect.width / 2
  const centerY = rect.top + rect.height / 2

  const move = (e) => {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    const clientY = e.touches ? e.touches[0].clientY : e.clientY
    
    const dx = clientX - centerX
    const dy = clientY - centerY
    
    let deg = Math.atan2(dy, dx) * (180 / Math.PI) + 90
    if (deg < 0) deg += 360
    
    emit('update:angle', Math.round(deg))
  }

  const up = () => {
    window.removeEventListener('mousemove', move)
    window.removeEventListener('mouseup', up)
    window.removeEventListener('touchmove', move)
    window.removeEventListener('touchend', up)
  }

  window.addEventListener('mousemove', move)
  window.addEventListener('mouseup', up)
  window.addEventListener('touchmove', move)
  window.addEventListener('touchend', up)
  move(e)
}
</script>
