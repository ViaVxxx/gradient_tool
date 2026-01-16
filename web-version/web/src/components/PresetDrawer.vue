<template>
  <Teleport to="body">
    <Transition name="drawer">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-50 flex items-end justify-center bg-black/50 backdrop-blur-sm"
        @click.self="$emit('close')">

        <div class="bg-white dark:bg-gray-900 rounded-t-3xl shadow-2xl w-full max-w-4xl max-h-[80vh] overflow-hidden">

          <!-- Header -->
          <div class="sticky top-0 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 p-6 z-10">
            <div class="flex items-center justify-between">
              <div>
                <h2 class="text-xl font-bold text-gray-900 dark:text-white">预设库</h2>
                <p class="text-sm text-gray-500 mt-1">选择一个预设快速开始</p>
              </div>

              <div class="flex items-center gap-3">
                <!-- 分类筛选 -->
                <select
                  v-model="selectedCategory"
                  class="text-sm border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 bg-white dark:bg-gray-800 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500">
                  <option value="">全部分类</option>
                  <option value="nature">自然</option>
                  <option value="sunset">日落</option>
                  <option value="ocean">海洋</option>
                  <option value="abstract">抽象</option>
                </select>

                <!-- 关闭按钮 -->
                <button
                  @click="$emit('close')"
                  class="p-2 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors">
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- 预设网格 -->
          <div class="p-6 overflow-y-auto" style="max-height: calc(80vh - 100px);">
            <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <button
                v-for="preset in filteredPresets"
                :key="preset.name"
                @click="selectPreset(preset)"
                class="group relative h-32 rounded-xl overflow-hidden border-2 border-gray-200 dark:border-gray-700 hover:border-indigo-400 dark:hover:border-indigo-500 transition-all duration-200 shadow-sm hover:shadow-lg">

                <!-- 预设预览 -->
                <div
                  class="absolute inset-0"
                  :style="getPresetStyle(preset)">
                </div>

                <!-- 悬停信息 -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex flex-col justify-end p-4">
                  <div class="text-left">
                    <div class="text-sm text-white font-semibold truncate">{{ preset.name }}</div>
                    <div class="text-xs text-white/80 mt-1">{{ preset.category || '未分类' }}</div>
                    <div class="text-xs text-white/60 mt-1">{{ preset.stops.length }} 色标</div>
                  </div>
                </div>

                <!-- 选中指示器 -->
                <div class="absolute top-3 right-3 w-8 h-8 rounded-full bg-white/20 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <svg class="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                  </svg>
                </div>
              </button>
            </div>

            <!-- 空状态 -->
            <div v-if="filteredPresets.length === 0" class="text-center py-12">
              <svg class="w-16 h-16 mx-auto text-gray-300 dark:text-gray-600 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4" />
              </svg>
              <p class="text-gray-500 dark:text-gray-400">该分类下暂无预设</p>
            </div>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useGradient } from '@/composables/useGradient'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'select'])

const { presets, loadPreset, rgbToHex } = useGradient()

const selectedCategory = ref('')

const filteredPresets = computed(() => {
  if (!selectedCategory.value) return presets.value
  return presets.value.filter(preset => preset.category === selectedCategory.value)
})

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

function selectPreset(preset) {
  loadPreset(preset)
  emit('select', preset)
  emit('close')
}
</script>

<style scoped>
.drawer-enter-active,
.drawer-leave-active {
  transition: all 300ms ease-out;
}

.drawer-enter-from,
.drawer-leave-to {
  opacity: 0;
}

.drawer-enter-from > div,
.drawer-leave-to > div {
  transform: translateY(100%);
}
</style>
