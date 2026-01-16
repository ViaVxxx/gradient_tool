<template>
  <div
    class="gradient-handle-container absolute top-0 bottom-0 transform -translate-x-1/2"
    :class="isSelected ? 'z-30' : 'z-20'"
    :style="{ left: (stop.position * 100) + '%' }">

    <!-- 胶囊型手柄 (物理模拟风格) -->
    <div
      class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 pointer-events-auto group/handle"
      @mousedown.stop.prevent="$emit('start-drag', $event)"
      @touchstart.stop.prevent="$emit('start-drag', $event)"
      @click.stop="$emit('select')"
      @mousedown.stop>

      <!-- 外层胶囊 -->
      <div
        :class="[
          'w-[14px] h-[30px] rounded-[6px] border-2 shadow-[0_2px_4px_rgba(0,0,0,0.2)] transition-all duration-200 cursor-ew-resize',
          isSelected
            ? 'border-gray-800 scale-110 shadow-lg'
            : 'border-white hover:scale-110'
        ]"
        :style="{ backgroundColor: stop.hex }">
      </div>

      <!-- 删除按钮 -->
      <button
        v-if="canDelete"
        @click.stop="$emit('delete')"
        class="absolute -top-2 -right-2 w-4 h-4 bg-red-500 text-white rounded-full text-[10px] opacity-0 group-hover/handle:opacity-100 transition-opacity flex items-center justify-center hover:bg-red-600 shadow-sm z-40">
        ×
      </button>
    </div>

    <!-- 浮动输入框 (仅选中时显示) -->
    <Transition name="floating-input">
      <div
        v-if="isSelected"
        class="floating-input absolute top-full left-1/2 -translate-x-1/2 mt-1 pointer-events-auto"
        @click.stop>

        <!-- 输入框 -->
        <input
          type="number"
          :value="Math.round(stop.position * 100)"
          @input="handlePositionInput"
          @keydown.enter="$event.target.blur()"
          @keydown.up.prevent="adjustPosition(1)"
          @keydown.down.prevent="adjustPosition(-1)"
          min="0"
          max="100"
          class="w-14 px-2 py-1 bg-white border border-gray-200 rounded shadow-xl text-xs font-mono text-center focus:outline-none focus:ring-2 focus:ring-indigo-500"
          placeholder="0">
        <span class="absolute right-1 top-1/2 -translate-y-1/2 text-[10px] text-gray-400 pointer-events-none">%</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
const props = defineProps({
  stop: {
    type: Object,
    required: true
  },
  isSelected: {
    type: Boolean,
    default: false
  },
  canDelete: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['select', 'delete', 'start-drag', 'update-position'])

function handlePositionInput(event) {
  let value = parseInt(event.target.value)
  if (isNaN(value)) return

  value = Math.max(0, Math.min(100, value))
  const position = value / 100
  emit('update-position', position)
}

function adjustPosition(delta) {
  const currentPercent = Math.round(props.stop.position * 100)
  const newPercent = Math.max(0, Math.min(100, currentPercent + delta))
  emit('update-position', newPercent / 100)
}
</script>

<style scoped>
/* 浮动输入框动画 */
.floating-input-enter-active,
.floating-input-leave-active {
  transition: all 200ms ease-out;
}

.floating-input-enter-from,
.floating-input-leave-to {
  opacity: 0;
  transform: translateX(-50%) translateY(-5px);
}

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
