<template>
  <div class="stops-list-container space-y-3">
    <!-- Header -->
    <div class="flex items-center justify-between mb-2">
      <h4 class="text-sm font-semibold text-gray-800 dark:text-gray-200">色标列表</h4>
      <span class="text-xs text-gray-500">{{ stops.length }}/20</span>
    </div>

    <!-- List -->
    <div class="space-y-2 max-h-64 overflow-y-auto overflow-x-hidden no-scrollbar">
      <div
        v-for="(stop, index) in stops"
        :key="index"
        :class="[
          'stops-list-item grid grid-cols-[32px_minmax(70px,1fr)_55px_24px] gap-1.5 items-center px-2 py-2 rounded-lg transition-all duration-200 cursor-pointer',
          selectedIndex === index
            ? 'bg-blue-50 dark:bg-blue-900/20 ring-2 ring-blue-500'
            : 'bg-gray-50 dark:bg-gray-800/50 hover:bg-gray-100 dark:hover:bg-gray-800'
        ]"
        @click="$emit('select', index)">

        <!-- 颜色预览方块 -->
        <div
          class="w-8 h-8 rounded-lg border-2 border-white shadow-md ring-1 ring-gray-200 dark:ring-gray-600 cursor-pointer hover:ring-2 hover:ring-indigo-500 transition-all flex-shrink-0"
          :style="{ backgroundColor: stop.hex }"
          @click.stop="$emit('select', index)">
        </div>

        <!-- HEX 输入框 -->
        <input
          type="text"
          :value="stop.hex"
          @input="handleHexInput(index, $event)"
          @blur="handleHexBlur(index, $event)"
          @click.stop
          @focus="$emit('select', index)"
          :class="[
            'px-1.5 py-1 text-xs font-mono bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border rounded focus:outline-none focus:ring-1 transition-colors',
            hexErrors[index]
              ? 'border-red-500 focus:ring-red-500 bg-red-50 dark:bg-red-900/20'
              : 'border-gray-300 dark:border-gray-600 focus:ring-indigo-500'
          ]"
          placeholder="#000000">

        <!-- 位置百分比输入框 -->
        <div class="relative">
          <input
            type="number"
            :value="Math.round(stop.position * 100)"
            @input="handlePositionInput(index, $event)"
            @click.stop
            @focus="$emit('select', index)"
            min="0"
            max="100"
            class="w-full px-1.5 py-1 pr-5 text-xs font-medium text-center bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 border border-gray-300 dark:border-gray-600 rounded focus:outline-none focus:ring-1 focus:ring-indigo-500"
            placeholder="0">
          <span class="absolute right-1 top-1/2 -translate-y-1/2 text-[10px] text-gray-400 pointer-events-none font-medium">%</span>
        </div>

        <!-- 删除按钮 -->
        <button
          v-if="stops.length > 2"
          @click.stop="$emit('delete', index)"
          class="w-6 h-6 flex items-center justify-center rounded text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors flex-shrink-0">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
        <div v-else class="w-6 flex-shrink-0"></div>
      </div>
    </div>

    <!-- 添加按钮 -->
    <button
      @click="$emit('add')"
      :disabled="stops.length >= 20"
      class="w-full py-2 px-3 text-sm font-medium text-indigo-600 bg-indigo-50 hover:bg-indigo-100 dark:bg-indigo-900/20 dark:hover:bg-indigo-900/30 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2">
      <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
      </svg>
      添加色标
    </button>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  stops: {
    type: Array,
    required: true
  },
  selectedIndex: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['select', 'update:stop', 'delete', 'add'])

// 错误状态管理
const hexErrors = ref({})
const lastValidHex = ref({})

// 监听 stops 变化，初始化 lastValidHex
watch(() => props.stops, (newStops) => {
  newStops.forEach((stop, index) => {
    if (!lastValidHex.value[index]) {
      lastValidHex.value[index] = stop.hex
    }
  })
}, { immediate: true, deep: true })

function handleHexInput(index, event) {
  let hex = event.target.value.trim()

  // 自动补全 #
  if (hex && !hex.startsWith('#')) {
    hex = '#' + hex
  }

  // 实时验证 HEX 格式
  const isValid = /^#[0-9A-Fa-f]{6}$/.test(hex)

  if (isValid) {
    // 格式正确，清除错误状态并更新
    hexErrors.value[index] = false
    lastValidHex.value[index] = hex
    emit('update:stop', index, { hex })
  } else if (hex === '' || hex === '#') {
    // 允许清空或只输入 #
    hexErrors.value[index] = false
  } else {
    // 格式错误，显示错误状态
    hexErrors.value[index] = true
  }
}

function handleHexBlur(index, event) {
  const hex = event.target.value.trim()

  // 失焦时，如果格式不正确，回退到上一个有效值
  if (!hex || !/^#[0-9A-Fa-f]{6}$/.test(hex)) {
    hexErrors.value[index] = false
    // 回退到上一个有效值
    event.target.value = lastValidHex.value[index] || props.stops[index].hex
    emit('update:stop', index, { hex: lastValidHex.value[index] || props.stops[index].hex })
  }
}

function handlePositionInput(index, event) {
  let value = parseInt(event.target.value)

  // 边界验证
  if (isNaN(value)) {
    value = 0
  }

  // 严格限制在 0-100 范围内
  value = Math.max(0, Math.min(100, value))

  const position = value / 100
  emit('update:stop', index, { position })
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
