<template>
  <div class="relative h-24 select-none mb-6">
    <!-- Gradient Track -->
    <div 
      ref="trackRef"
      class="absolute top-4 left-0 right-0 h-4 rounded-full border-2 border-gray-200 dark:border-gray-600 cursor-crosshair shadow-inner"
      :style="previewStyle"
      @mousedown.self="addStop"
    >
      <!-- Grid/Ticks (Optional, keeping it clean for now) -->
    </div>

    <!-- Handles -->
    <div
      v-for="(stop, index) in stops"
      :key="index"
      class="absolute top-4 h-4 w-0"
      :style="{ left: stop.position * 100 + '%' }"
    >
      <!-- Capsule Handle -->
      <div
        class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-4 h-10 rounded-full border-2 border-white bg-transparent shadow-md cursor-grab active:cursor-grabbing hover:scale-110 transition-transform z-10 flex items-center justify-center group"
        :class="{ 'z-20 ring-2 ring-offset-2 ring-indigo-500 scale-105': selectedIndex === index }"
        @mousedown.stop="startDrag(index, $event)"
      >
        <!-- Inner Color Display -->
        <div 
          class="w-full h-full rounded-full" 
          :style="{ backgroundColor: stop.hex, opacity: stop.alpha / 100 }"
        ></div>
      </div>

      <!-- Floating Input (Only for Selected) -->
      <div 
        v-if="selectedIndex === index"
        class="absolute top-8 left-1/2 -translate-x-1/2 pt-2 z-30"
        @mousedown.stop
      >
        <!-- Arrow -->
        <div class="absolute -top-0 left-1/2 -translate-x-1/2 w-0 h-0 border-l-[6px] border-l-transparent border-r-[6px] border-r-transparent border-b-[6px] border-b-white filter drop-shadow-sm"></div>
        
        <!-- Input Box -->
        <div class="bg-white dark:bg-gray-800 rounded-md shadow-lg border border-gray-200 dark:border-gray-700 p-1 flex items-center">
          <input
            type="number"
            min="0"
            max="100"
            :value="Math.round(stop.position * 100)"
            @input="updatePositionInput(index, $event)"
            class="w-12 text-center text-xs font-mono border-none focus:ring-0 p-0 bg-transparent text-gray-900 dark:text-gray-100"
          />
          <span class="text-xs text-gray-400 mr-1">%</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  stops: {
    type: Array,
    required: true
  },
  selectedIndex: {
    type: Number,
    default: null
  },
  gradientType: {
    type: String,
    default: 'linear'
  },
  angle: {
    type: Number,
    default: 90
  }
})

const emit = defineEmits(['update:stop', 'select', 'add'])

const trackRef = ref(null)

const previewStyle = computed(() => {
  const stopsStr = props.stops
    .slice()
    .sort((a, b) => a.position - b.position)
    .map(s => `${s.hex} ${s.position * 100}%`)
    .join(', ')
  
  return {
    background: props.gradientType === 'linear' 
      ? `linear-gradient(90deg, ${stopsStr})` // Always horizontal for the track preview
      : `linear-gradient(90deg, ${stopsStr})`
  }
})

function addStop(e) {
  if (!trackRef.value) return
  const rect = trackRef.value.getBoundingClientRect()
  const x = e.clientX - rect.left
  const pos = Math.max(0, Math.min(1, x / rect.width))
  emit('add', pos)
}

function updatePositionInput(index, e) {
  let val = parseFloat(e.target.value)
  if (isNaN(val)) return
  val = Math.max(0, Math.min(100, val)) / 100
  emit('update:stop', index, { position: val })
}

function startDrag(index, e) {
  emit('select', index)
  
  const track = trackRef.value
  const rect = track.getBoundingClientRect()
  
  const moveHandler = (moveEvent) => {
    const clientX = moveEvent.touches ? moveEvent.touches[0].clientX : moveEvent.clientX
    const x = clientX - rect.left
    const pos = Math.max(0, Math.min(1, x / rect.width))
    // Round to 2 decimal places
    const roundedPos = Math.round(pos * 1000) / 1000
    
    emit('update:stop', index, { position: roundedPos })
  }

  const upHandler = () => {
    document.removeEventListener('mousemove', moveHandler)
    document.removeEventListener('mouseup', upHandler)
    document.removeEventListener('touchmove', moveHandler)
    document.removeEventListener('touchend', upHandler)
  }

  document.addEventListener('mousemove', moveHandler)
  document.addEventListener('mouseup', upHandler)
  document.addEventListener('touchmove', moveHandler)
  document.addEventListener('touchend', upHandler)
}
</script>
