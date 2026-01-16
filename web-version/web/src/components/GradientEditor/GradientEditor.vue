<template>
  <div class="bg-white/90 backdrop-blur-xl rounded-xl border border-gray-200/60 p-6 shadow-lg shadow-gray-200/40">
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-lg font-bold text-gray-800 flex items-center gap-2">
        <span class="w-1.5 h-6 bg-indigo-500 rounded-full"></span>
        Gradient Editor
      </h3>
      <div class="text-xs text-gray-500 font-mono">{{ colorStops.length }} stops</div>
    </div>

    <!-- Track -->
    <GradientTrack
      :stops="colorStops"
      :selected-index="selectedColorStopIndex"
      :gradient-type="gradientType"
      :angle="angle"
      @update:stop="updateStop"
      @select="selectStop"
      @add="addStop"
    />

    <!-- Controls -->
    <div class="mt-8 mb-6">
      <ControlPanel
        :type="gradientType"
        :angle="angle"
        @update:type="gradientType = $event"
        @update:angle="angle = $event"
      />
    </div>

    <!-- Bottom Section: List + Picker -->
    <div class="flex flex-col lg:flex-row gap-6 h-[320px]">
      <!-- List (Flexible) -->
      <div class="flex-1 min-h-0">
        <StopsList
          :stops="colorStops"
          :selected-index="selectedColorStopIndex"
          @select="selectStop"
          @update:stop="updateStop"
          @delete="removeStop"
        />
      </div>

      <!-- Picker (Fixed) -->
      <div class="w-full lg:w-[280px] flex-shrink-0 flex justify-center bg-gray-50 dark:bg-gray-800/50 rounded-lg border border-gray-100 dark:border-gray-700/50 p-4">
        <ColorPicker
          v-if="selectedStop"
          :color="selectedStop.color"
          :alpha="selectedStop.alpha"
          @update:color="updateSelectedColor"
          @update:alpha="updateSelectedAlpha"
        />
        <div v-else class="flex items-center justify-center text-gray-400 text-sm h-full">
          Select a stop to edit color
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useGradient, interpolateColorAtPosition } from '@/composables/useGradient'
import GradientTrack from './GradientTrack.vue'
import StopsList from './StopsList.vue'
import ColorPicker from './ColorPicker.vue'
import ControlPanel from './ControlPanel.vue'
import { rgbToHex, hexToRgb } from '@/utils/color'

const {
  colorStops,
  selectedColorStopIndex,
  gradientType,
  angle
} = useGradient()

const selectedStop = computed(() => {
  if (selectedColorStopIndex.value === null || !colorStops.value[selectedColorStopIndex.value]) return null
  return colorStops.value[selectedColorStopIndex.value]
})

function selectStop(index) {
  selectedColorStopIndex.value = index
}

function updateStop(index, changes) {
  const stop = colorStops.value[index]
  if (!stop) return
  
  if (changes.position !== undefined) {
    stop.position = changes.position
  }
  
  if (changes.hex) {
    stop.hex = changes.hex
    const rgb = hexToRgb(changes.hex)
    if (rgb) stop.color = rgb
  }
}

function updateSelectedColor(rgb) {
  if (!selectedStop.value) return
  selectedStop.value.color = rgb
  selectedStop.value.hex = rgbToHex(rgb.r, rgb.g, rgb.b)
}

function updateSelectedAlpha(alpha) {
  if (!selectedStop.value) return
  selectedStop.value.alpha = alpha
}

function addStop(position) {
  if (colorStops.value.length >= 20) return

  const interpolatedColor = interpolateColorAtPosition(colorStops.value, position)
  
  const newStop = {
    position: parseFloat(position.toFixed(2)),
    color: interpolatedColor,
    hex: rgbToHex(interpolatedColor.r, interpolatedColor.g, interpolatedColor.b),
    alpha: 100
  }
  
  // Find insertion index
  let insertIndex = colorStops.value.findIndex(stop => stop.position > position)
  if (insertIndex === -1) insertIndex = colorStops.value.length
  
  colorStops.value.splice(insertIndex, 0, newStop)
  selectedColorStopIndex.value = insertIndex
}

function removeStop(index) {
  if (colorStops.value.length <= 2) return
  
  colorStops.value.splice(index, 1)
  
  if (selectedColorStopIndex.value >= colorStops.value.length) {
    selectedColorStopIndex.value = colorStops.value.length - 1
  }
}
</script>