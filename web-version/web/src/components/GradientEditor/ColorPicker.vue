<template>
  <div class="flex flex-col gap-4 w-full max-w-[280px]">
    <!-- Saturation/Value Picker (256x256 equivalent aspect ratio) -->
    <div 
      class="relative w-full aspect-square rounded-lg overflow-hidden cursor-crosshair shadow-sm border border-gray-200"
      :style="{ backgroundColor: `hsl(${hsv.h}, 100%, 50%)` }"
      @mousedown="startDragSV"
      ref="svRef"
    >
      <!-- White Gradient (Horizontal) -->
      <div class="absolute inset-0" style="background: linear-gradient(to right, #fff, transparent)"></div>
      <!-- Black Gradient (Vertical) -->
      <div class="absolute inset-0" style="background: linear-gradient(to top, #000, transparent)"></div>
      
      <!-- Cursor -->
      <div 
        class="absolute w-4 h-4 rounded-full border-2 border-white shadow-md -translate-x-1/2 -translate-y-1/2 pointer-events-none"
        :style="{ 
          left: `${hsv.s}%`, 
          top: `${100 - hsv.v}%`,
          backgroundColor: hex
        }"
      ></div>
    </div>

    <!-- Sliders -->
    <div class="space-y-3">
      <!-- Hue Slider -->
      <div class="relative h-4 rounded-full cursor-pointer shadow-inner" style="background: linear-gradient(to right, #f00, #ff0, #0f0, #0ff, #00f, #f0f, #f00)" @mousedown="startDragHue" ref="hueRef">
        <div 
          class="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-white rounded-full border border-gray-300 shadow transform -translate-x-1/2"
          :style="{ left: `${(hsv.h / 360) * 100}%` }"
        ></div>
      </div>

      <!-- Alpha Slider -->
      <div class="relative h-4 rounded-full cursor-pointer shadow-inner bg-[url('data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAYAAADED76LAAAAH0lEQVQYV2NkYGAwZmBg8GfAAjdRwzAAphhCGB0XjAAAGy8H/az6ZwAAAAAASUVORK5CYII=')]" @mousedown="startDragAlpha" ref="alphaRef">
        <div class="absolute inset-0 rounded-full" :style="{ background: `linear-gradient(to right, transparent, ${hex})` }"></div>
        <div 
          class="absolute top-1/2 -translate-y-1/2 w-4 h-4 bg-white rounded-full border border-gray-300 shadow transform -translate-x-1/2"
          :style="{ left: `${alpha}%` }"
        ></div>
      </div>
    </div>

    <!-- Inputs -->
    <div class="grid grid-cols-4 gap-2 text-xs">
      <!-- Hex -->
      <div class="col-span-4 flex items-center border border-gray-300 rounded px-2 py-1 bg-white">
        <span class="text-gray-400 mr-2">#</span>
        <input 
          type="text" 
          v-model.lazy="hexInput"
          @change="updateFromHex"
          class="w-full uppercase font-mono bg-transparent outline-none"
        />
      </div>
      
      <!-- RGBA -->
      <div class="col-span-1 border border-gray-300 rounded px-1 py-1 text-center bg-white">
        <input type="number" v-model.number="rgbInput.r" @input="updateFromRgb" class="w-full text-center outline-none bg-transparent no-arrows" />
        <span class="text-[10px] text-gray-400 block mt-0.5">R</span>
      </div>
      <div class="col-span-1 border border-gray-300 rounded px-1 py-1 text-center bg-white">
        <input type="number" v-model.number="rgbInput.g" @input="updateFromRgb" class="w-full text-center outline-none bg-transparent no-arrows" />
        <span class="text-[10px] text-gray-400 block mt-0.5">G</span>
      </div>
      <div class="col-span-1 border border-gray-300 rounded px-1 py-1 text-center bg-white">
        <input type="number" v-model.number="rgbInput.b" @input="updateFromRgb" class="w-full text-center outline-none bg-transparent no-arrows" />
        <span class="text-[10px] text-gray-400 block mt-0.5">B</span>
      </div>
      <div class="col-span-1 border border-gray-300 rounded px-1 py-1 text-center bg-white">
        <input type="number" :value="alpha" @input="updateAlphaInput" class="w-full text-center outline-none bg-transparent no-arrows" />
        <span class="text-[10px] text-gray-400 block mt-0.5">A</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { rgbToHsv, hsvToRgb, rgbToHex, hexToRgb } from '@/utils/color'

const props = defineProps({
  color: { type: Object, required: true }, // { r, g, b }
  alpha: { type: Number, default: 100 }
})

const emit = defineEmits(['update:color', 'update:alpha'])

const svRef = ref(null)
const hueRef = ref(null)
const alphaRef = ref(null)

const hsv = ref({ h: 0, s: 0, v: 100 })
const rgbInput = ref({ r: 0, g: 0, b: 0 })
const hexInput = ref('')

// Watch for prop changes to update internal state (if not dragging ideally, but simple sync for now)
watch(() => props.color, (newColor) => {
  const newHsv = rgbToHsv(newColor.r, newColor.g, newColor.b)
  // Only update if significantly different to avoid jitter during drag
  // Actually, for a controlled component, we should always sync unless we are the source of change.
  // For simplicity, we sync.
  hsv.value = newHsv
  rgbInput.value = { ...newColor }
  hexInput.value = rgbToHex(newColor.r, newColor.g, newColor.b).replace('#', '')
}, { immediate: true, deep: true })

const hex = computed(() => '#' + hexInput.value)

function emitColor() {
  const rgb = hsvToRgb(hsv.value.h, hsv.value.s, hsv.value.v)
  emit('update:color', rgb)
}

function updateFromHex(e) {
  const val = e.target.value
  const rgb = hexToRgb(val)
  if (rgb) {
    emit('update:color', rgb)
  }
}

function updateFromRgb() {
  emit('update:color', { r: rgbInput.value.r, g: rgbInput.value.g, b: rgbInput.value.b })
}

function updateAlphaInput(e) {
  let val = parseInt(e.target.value)
  if (isNaN(val)) val = 100
  emit('update:alpha', Math.max(0, Math.min(100, val)))
}

// Drag Handlers
function startDragSV(e) {
  const rect = svRef.value.getBoundingClientRect()
  
  const move = (e) => {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    const clientY = e.touches ? e.touches[0].clientY : e.clientY
    
    let s = (clientX - rect.left) / rect.width * 100
    let v = 100 - (clientY - rect.top) / rect.height * 100
    
    s = Math.max(0, Math.min(100, s))
    v = Math.max(0, Math.min(100, v))
    
    hsv.value.s = s
    hsv.value.v = v
    emitColor()
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
  move(e) // Trigger once immediately
}

function startDragHue(e) {
  const rect = hueRef.value.getBoundingClientRect()
  
  const move = (e) => {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    let h = (clientX - rect.left) / rect.width * 360
    h = Math.max(0, Math.min(360, h))
    hsv.value.h = h
    emitColor()
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

function startDragAlpha(e) {
  const rect = alphaRef.value.getBoundingClientRect()
  
  const move = (e) => {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    let a = (clientX - rect.left) / rect.width * 100
    a = Math.max(0, Math.min(100, a))
    emit('update:alpha', Math.round(a))
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

<style scoped>
.no-arrows::-webkit-inner-spin-button,
.no-arrows::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.no-arrows {
  -moz-appearance: textfield;
}
</style>
