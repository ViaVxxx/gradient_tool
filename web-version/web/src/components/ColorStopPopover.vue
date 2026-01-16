<template>
  <Teleport to="body">
    <Transition name="popover">
      <div
        v-if="show"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        @click.self="$emit('close')">

        <div class="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-6 w-80 max-w-full">

          <!-- Header -->
          <div class="flex items-center justify-between mb-4">
            <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300">
              编辑色标 #{{ index + 1 }}
            </h4>
            <button
              @click="$emit('close')"
              class="p-1 rounded-lg text-gray-400 hover:text-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- 颜色选择器 -->
          <div class="mb-4">
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">颜色</label>
            <div class="relative">
              <!-- 大色块显示 -->
              <div
                class="w-full h-32 rounded-xl border-2 border-gray-200 dark:border-gray-600 cursor-pointer relative overflow-hidden shadow-inner hover:shadow-lg transition-shadow"
                :style="{ backgroundColor: localStop.hex }"
                @click="$refs.colorPicker.click()">

                <!-- 隐藏的颜色输入 -->
                <input
                  ref="colorPicker"
                  type="color"
                  v-model="localStop.hex"
                  @input="updateColorFromHex"
                  class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">

                <!-- 选择指示器 -->
                <div class="absolute inset-0 flex items-center justify-center">
                  <div class="w-12 h-12 rounded-full border-2 border-white/60 flex items-center justify-center backdrop-blur-sm">
                    <svg class="w-6 h-6 text-white/80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- HEX 输入 -->
          <div class="mb-4">
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">HEX</label>
            <input
              type="text"
              v-model="localStop.hex"
              @input="updateColorFromHex"
              class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-mono bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-indigo-500"
              placeholder="#8FCF72">
          </div>

          <!-- RGB 输入 -->
          <div class="mb-4">
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-1">RGB</label>
            <div class="grid grid-cols-3 gap-2">
              <div>
                <input
                  type="number"
                  v-model.number="localStop.color.r"
                  @input="updateHexFromRgb"
                  min="0" max="255"
                  class="w-full px-2 py-2 border border-gray-300 dark:border-gray-600 rounded text-sm text-center bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-1 focus:ring-indigo-500">
                <span class="block text-xs text-gray-400 text-center mt-1">R</span>
              </div>
              <div>
                <input
                  type="number"
                  v-model.number="localStop.color.g"
                  @input="updateHexFromRgb"
                  min="0" max="255"
                  class="w-full px-2 py-2 border border-gray-300 dark:border-gray-600 rounded text-sm text-center bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-1 focus:ring-indigo-500">
                <span class="block text-xs text-gray-400 text-center mt-1">G</span>
              </div>
              <div>
                <input
                  type="number"
                  v-model.number="localStop.color.b"
                  @input="updateHexFromRgb"
                  min="0" max="255"
                  class="w-full px-2 py-2 border border-gray-300 dark:border-gray-600 rounded text-sm text-center bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-1 focus:ring-indigo-500">
                <span class="block text-xs text-gray-400 text-center mt-1">B</span>
              </div>
            </div>
          </div>

          <!-- 位置调整 -->
          <div class="mb-4">
            <label class="block text-xs font-medium text-gray-600 dark:text-gray-400 mb-2">
              位置: {{ Math.round(localStop.position * 100) }}%
            </label>
            <input
              type="range"
              v-model.number="localStop.position"
              min="0" max="1" step="0.01"
              class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider">
          </div>

          <!-- 操作按钮 -->
          <div class="flex gap-2">
            <button
              v-if="colorStops.length > 2"
              @click="$emit('delete')"
              class="flex-1 px-4 py-2 rounded-lg bg-red-50 text-red-600 hover:bg-red-100 dark:bg-red-900/20 dark:text-red-400 dark:hover:bg-red-900/30 text-sm font-medium transition-colors">
              删除
            </button>
            <button
              @click="applyChanges"
              class="flex-1 px-4 py-2 rounded-lg bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white text-sm font-semibold transition-all shadow-lg">
              应用
            </button>
          </div>

        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useGradient } from '@/composables/useGradient'

const props = defineProps({
  stop: {
    type: Object,
    required: true
  },
  index: {
    type: Number,
    required: true
  }
})

const emit = defineEmits(['close', 'update', 'delete'])

const { colorStops, hexToRgb, rgbToHex } = useGradient()

const show = ref(true)
const localStop = ref({ ...props.stop })

// 监听 props 变化
watch(() => props.stop, (newStop) => {
  localStop.value = { ...newStop }
}, { deep: true })

function updateColorFromHex() {
  const rgb = hexToRgb(localStop.value.hex)
  if (rgb) {
    localStop.value.color = rgb
  }
}

function updateHexFromRgb() {
  localStop.value.hex = rgbToHex(
    localStop.value.color.r,
    localStop.value.color.g,
    localStop.value.color.b
  )
}

function applyChanges() {
  emit('update', props.index, localStop.value)
  emit('close')
}
</script>

<style scoped>
.popover-enter-active,
.popover-leave-active {
  transition: all 200ms ease-out;
}

.popover-enter-from,
.popover-leave-to {
  opacity: 0;
}

.popover-enter-from > div,
.popover-leave-to > div {
  transform: scale(0.95);
}
</style>
