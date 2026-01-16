<template>
  <div class="flex flex-col h-full bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
    <!-- Header -->
    <div class="px-3 py-2 bg-gray-50 dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 text-xs font-semibold text-gray-500 uppercase flex">
      <div class="w-8">Color</div>
      <div class="flex-1 px-2">Hex</div>
      <div class="w-16 text-center">Pos</div>
      <div class="w-8"></div>
    </div>

    <!-- Scrollable List -->
    <div class="flex-1 overflow-y-auto custom-scrollbar">
      <div 
        v-for="(stop, index) in stops" 
        :key="index"
        class="flex items-center px-3 py-2 border-b border-gray-100 dark:border-gray-700/50 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors cursor-pointer group"
        :class="{ 'bg-blue-50 dark:bg-blue-900/20': selectedIndex === index }"
        @click="$emit('select', index)"
      >
        <!-- Color Preview -->
        <div class="w-8 flex-shrink-0">
          <div 
            class="w-6 h-6 rounded border border-gray-200 shadow-sm"
            :style="{ backgroundColor: stop.hex }"
          ></div>
        </div>

        <!-- Hex Input -->
        <div class="flex-1 px-2">
          <input 
            type="text" 
            :value="stop.hex"
            @change="updateHex(index, $event)"
            class="w-full text-sm font-mono bg-transparent border-none focus:ring-0 p-0 text-gray-700 dark:text-gray-200 uppercase"
          />
        </div>

        <!-- Position Input -->
        <div class="w-16 flex-shrink-0">
          <div class="relative">
            <input 
              type="number" 
              min="0" 
              max="100"
              :value="Math.round(stop.position * 100)"
              @input="updatePos(index, $event)"
              class="w-full text-right text-sm font-mono bg-transparent border-gray-200 rounded px-1 py-0.5 focus:ring-1 focus:ring-blue-500"
            />
            <span class="absolute right-6 top-0.5 text-xs text-transparent pointer-events-none">%</span>
          </div>
        </div>

        <!-- Delete Button -->
        <div class="w-8 flex justify-end">
          <button 
            @click.stop="$emit('delete', index)"
            class="text-gray-400 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-opacity"
            title="Remove stop"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  stops: Array,
  selectedIndex: Number
})

const emit = defineEmits(['select', 'update:stop', 'delete'])

function updateHex(index, e) {
  const hex = e.target.value
  if (/^#[0-9A-F]{6}$/i.test(hex)) {
    emit('update:stop', index, { hex })
  }
}

function updatePos(index, e) {
  let val = parseFloat(e.target.value)
  if (isNaN(val)) return
  val = Math.max(0, Math.min(100, val)) / 100
  emit('update:stop', index, { position: val })
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 2px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
</style>
