<template>
  <div class="flex items-center justify-between gap-4 p-4 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 shadow-sm">
    <!-- Type Selector -->
    <div class="flex p-1 bg-gray-100 dark:bg-gray-700 rounded-lg">
      <button
        v-for="t in ['linear', 'radial']"
        :key="t"
        class="px-4 py-1.5 text-sm font-medium rounded-md transition-all capitalize"
        :class="type === t ? 'bg-white dark:bg-gray-600 shadow text-indigo-600 dark:text-indigo-400' : 'text-gray-500 hover:text-gray-700 dark:text-gray-400'"
        @click="$emit('update:type', t)"
      >
        {{ t }}
      </button>
    </div>

    <!-- Angle Control (Visible only for Linear) -->
    <div 
      v-if="type === 'linear'"
      class="flex items-center gap-3"
    >
      <div class="flex items-center gap-2">
        <input 
          type="number" 
          :value="angle"
          @input="onAngleInput"
          class="w-16 text-right px-2 py-1 text-sm border border-gray-300 dark:border-gray-600 rounded bg-transparent focus:ring-1 focus:ring-indigo-500"
        />
        <span class="text-sm text-gray-500">deg</span>
      </div>

      <!-- Dial -->
      <div 
        class="relative w-8 h-8 cursor-pointer group"
        @mousedown="startAngleDrag"
      >
        <svg class="w-full h-full text-gray-300 dark:text-gray-600 group-hover:text-gray-400 transition-colors" viewBox="0 0 32 32">
          <circle cx="16" cy="16" r="15" fill="none" stroke="currentColor" stroke-width="2" />
        </svg>
        <div 
          class="absolute top-1/2 left-1/2 w-full h-0.5 bg-indigo-500 origin-left transform -translate-y-1/2 pointer-events-none"
          :style="{ transform: `translateY(-50%) rotate(${angle - 90}deg)`, width: '12px' }"
        >
          <div class="absolute right-0 top-1/2 -translate-y-1/2 w-2 h-2 bg-indigo-500 rounded-full"></div>
        </div>
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
