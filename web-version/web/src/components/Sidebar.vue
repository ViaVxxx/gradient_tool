<template>
  <aside
    class="w-80 h-full bg-white/80 dark:bg-slate-900/50 backdrop-blur-2xl border-r border-white/10 shadow-[4px_0_24px_rgba(0,0,0,0.2)] overflow-y-auto no-scrollbar sidebar-transition fixed lg:relative z-30"
    :class="{ 
      '-translate-x-full': isPureMode || !isSidebarOpen,
      'lg:-ml-80': isPureMode || !isSidebarOpen 
    }">

    <!-- Header -->
    <div class="p-6 border-b border-white/10">
      <div class="flex items-center space-x-3">
        <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg ring-2 ring-indigo-400/30">
          <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
          </svg>
        </div>
        <div>
          <h1 class="text-lg font-bold text-gray-900 dark:text-white">Gradient Studio</h1>
          <p class="text-xs text-gray-500 dark:text-gray-400">专业渐变设计工具</p>
        </div>
      </div>
    </div>

    <!-- Content Sections -->
    <div class="p-4 space-y-4">

      <!-- 色标编辑 - 使用新的 GradientEditor -->
      <section class="space-y-3 animate-slide-in-left" style="animation-delay: 0.1s">
        <GradientEditor />
      </section>

      <!-- 纹理效果 -->
      <section class="space-y-3 animate-slide-in-left" style="animation-delay: 0.4s">
        <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 flex items-center">
          <svg class="w-4 h-4 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
          </svg>
          纹理效果
        </h3>

        <div class="space-y-2">
          <div
            v-for="effect in effects"
            :key="effect.value"
            class="p-3 rounded-lg border transition-all"
            :class="effectsEnabled[effect.value] ? 'border-indigo-300 bg-indigo-50/50 dark:bg-indigo-900/20' : 'border-gray-200 dark:border-gray-700 bg-gray-50/50 dark:bg-gray-800/50'">

            <div class="flex items-center justify-between mb-2">
              <label class="flex items-center gap-2 cursor-pointer">
                <input
                  type="checkbox"
                  v-model="effectsEnabled[effect.value]"
                  @change="toggleEffect(effect.value)"
                  class="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                <span class="text-sm font-medium" :class="effectsEnabled[effect.value] ? 'text-gray-900 dark:text-white' : 'text-gray-500'">
                  {{ effect.icon }} {{ effect.label }}
                </span>
              </label>
              <span v-if="effectsEnabled[effect.value]" class="text-xs font-mono font-semibold text-indigo-600">
                {{ Math.round(effectIntensities[effect.value] * 100) }}%
              </span>
            </div>

            <div v-if="effectsEnabled[effect.value]">
              <input
                type="range"
                v-model.number="effectIntensities[effect.value]"
                min="0.05"
                max="1"
                step="0.05"
                @input="onEffectIntensityChange(effect.value)"
                class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider">
            </div>
          </div>
        </div>
      </section>

      <!-- 预设库预览 -->
      <section class="space-y-3 animate-slide-in-left" style="animation-delay: 0.5s">
        <div class="flex items-center justify-between">
          <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300 flex items-center">
            <svg class="w-4 h-4 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
            预设
          </h3>
          <button
            @click="$emit('open-presets')"
            class="text-xs text-indigo-600 hover:text-indigo-700">
            查看更多 →
          </button>
        </div>

        <div class="grid grid-cols-2 gap-3">
          <button
            v-for="preset in presets.slice(0, 4)"
            :key="preset.name"
            @click="loadPreset(preset)"
            class="group relative h-24 rounded-xl overflow-hidden border-2 border-gray-200 dark:border-gray-700 hover:border-indigo-400 dark:hover:border-indigo-500 transition-all duration-300 hover:scale-105 hover:shadow-xl"
            :style="getPresetStyle(preset)">
            <!-- 悬停遮罩 -->
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
            <!-- 预设名称 -->
            <div class="absolute bottom-2 left-2 right-2 text-xs text-white font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300 truncate">
              {{ preset.name }}
            </div>
          </button>
        </div>
      </section>

    </div>
  </aside>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useGradient } from '@/composables/useGradient'
import GradientBar from './GradientBar.vue'
import GradientEditor from './GradientEditor.vue'

const {
  gradientType,
  angle,
  colorStops,
  effectsEnabled,
  effectIntensities,
  isPureMode,
  presets,
  loadPreset,
  applyEffect,
  resetToOriginalImage,
  rgbToHex,
  interpolateColorAtPosition
} = useGradient()

// 响应式侧边栏控制
const isSidebarOpen = ref(true)

// 监听窗口大小变化
function handleResize() {
  if (window.innerWidth < 1024) {
    isSidebarOpen.value = false
  } else {
    isSidebarOpen.value = true
  }
}

onMounted(() => {
  handleResize()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
})

// 暴露方法供父组件调用
defineExpose({
  toggleSidebar: () => {
    isSidebarOpen.value = !isSidebarOpen.value
  }
})

const gradientTypes = [
  { label: '线性', value: 'linear' },
  { label: '径向', value: 'radial' }
]

const effects = [
  { label: 'Perlin 噪点', value: 'perlin', icon: '✨' },
  { label: '磨砂玻璃', value: 'frosted', icon: '🌫️' },
  { label: '胶片颗粒', value: 'film', icon: '🎞️' },
  { label: '晕影效果', value: 'vignette', icon: '🎭' }
]

function addColorStop() {
  if (colorStops.value.length >= 20) return

  const newPosition = 0.5
  const interpolatedColor = interpolateColorAtPosition(colorStops.value, newPosition)

  const newStop = {
    position: newPosition,
    color: interpolatedColor,
    hex: rgbToHex(interpolatedColor.r, interpolatedColor.g, interpolatedColor.b),
    alpha: 100
  }

  colorStops.value.push(newStop)
}

function toggleEffect(effectType) {
  if (effectsEnabled.value[effectType]) {
    applyEffect(effectType)
  } else {
    // 当取消选中效果时，恢复到原始图像
    resetToOriginalImage()
  }
}

let debounceTimer = null
function onEffectIntensityChange(effectType) {
  if (debounceTimer) clearTimeout(debounceTimer)

  debounceTimer = setTimeout(() => {
    if (effectsEnabled.value[effectType]) {
      applyEffect(effectType)
    }
  }, 500)
}

function getPresetStyle(preset) {
  const stops = preset.stops.map(stop => {
    const { r, g, b } = stop.color
    return `rgb(${r},${g},${b}) ${stop.position * 100}%`
  }).join(', ')

  if (preset.gradient_type === 'linear') {
    return {
      background: `linear-gradient(${preset.angle || 90}deg, ${stops})`
    }
  } else {
    return {
      background: `radial-gradient(circle, ${stops})`
    }
  }
}
</script>
