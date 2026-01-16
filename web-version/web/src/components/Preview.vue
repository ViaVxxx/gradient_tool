<template>
  <main class="flex-1 h-full bg-checkerboard relative overflow-hidden">

    <!-- 预览画布 -->
    <div class="absolute inset-0 flex items-center justify-center">

      <!-- CSS 预览模式 -->
      <div
        v-if="previewMode === 'css' || !generatedImage"
        class="absolute inset-0"
        :style="previewStyle">
        <div class="absolute inset-0 flex items-center justify-center">
          <div class="text-center">
            <div class="w-16 h-16 mx-auto mb-4 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
              <svg class="w-8 h-8 text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
            <p class="text-sm text-white/80 font-medium">实时预览</p>
            <p class="text-xs text-white/60 mt-1">点击生成高质量图像</p>
          </div>
        </div>
      </div>

      <!-- 生成图像预览 -->
      <img
        v-if="previewMode === 'image' && generatedImage"
        :src="generatedImage"
        alt="Generated gradient"
        class="absolute inset-0 w-full h-full object-cover">

      <!-- 加载状态 -->
      <div v-if="isGenerating"
           class="absolute inset-0 bg-white/90 backdrop-blur-sm flex items-center justify-center">
        <div class="text-center">
          <div class="w-12 h-12 border-4 border-gray-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-4"></div>
          <p class="text-sm text-gray-700 font-medium">{{ loadingText }}</p>
          <div class="w-48 bg-gray-200 rounded-full h-1.5 mt-2">
            <div class="bg-indigo-600 h-1.5 rounded-full transition-all duration-300" :style="{ width: loadingProgress + '%' }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 移动端菜单按钮 -->
    <button
      @click="$emit('toggle-sidebar')"
      class="lg:hidden absolute top-6 left-6 z-20 p-3 smart-toolbar rounded-full text-white hover:bg-white/10 transition-colors shadow-2xl">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>

    <!-- 底部悬浮工具栏 -->
    <div class="absolute bottom-6 left-1/2 transform -translate-x-1/2 z-20 animate-slide-in-bottom">
      <div class="smart-toolbar rounded-2xl px-3 md:px-6 py-3 flex items-center gap-2 md:gap-4 shadow-2xl flex-wrap justify-center max-w-[90vw]">

        <!-- 纯净模式 (桌面端显示) -->
        <button
          @click="togglePureMode"
          class="hidden md:flex items-center justify-center p-2.5 rounded-xl text-white/90 hover:text-white hover:bg-white/20 transition-all duration-200"
          title="纯净模式">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
          </svg>
        </button>

        <!-- 预览模式切换 -->
        <div class="flex items-center bg-black/20 rounded-xl p-1 backdrop-blur-sm">
          <button
            @click="previewMode = 'css'"
            :class="[
              'px-2 md:px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200',
              previewMode === 'css' ? 'bg-white/30 text-white shadow-sm' : 'text-white/70 hover:text-white hover:bg-white/10'
            ]">
            CSS
          </button>
          <button
            @click="previewMode = 'image'"
            :class="[
              'px-2 md:px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-200',
              previewMode === 'image' ? 'bg-white/30 text-white shadow-sm' : 'text-white/70 hover:text-white hover:bg-white/10'
            ]">
            图像
          </button>
        </div>

        <!-- 分隔线 -->
        <div class="w-px h-6 bg-white/30"></div>

        <!-- 随机生成 -->
        <button
          @click="randomGradient"
          class="p-2.5 rounded-xl text-white/90 hover:text-white hover:bg-white/20 transition-all duration-200"
          title="随机生成">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
        </button>

        <!-- 生成按钮 -->
        <button
          @click="generateGradient"
          :disabled="isGenerating"
          class="px-4 md:px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 text-white text-sm font-semibold transition-all duration-200 disabled:opacity-50 shadow-lg hover:shadow-xl hover:scale-105">
          <span class="flex items-center gap-2">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            <span class="hidden sm:inline">{{ isGenerating ? loadingText : '生成' }}</span>
          </span>
        </button>

        <!-- 分隔线 -->
        <div class="w-px h-6 bg-white/30"></div>

        <!-- 复制 CSS -->
        <button
          @click="copyCSS"
          class="p-2.5 rounded-xl text-white/90 hover:text-white hover:bg-white/20 transition-all duration-200"
          title="复制 CSS">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
          </svg>
        </button>

        <!-- 导出 -->
        <button
          @click="exportImage"
          :disabled="!generatedImage"
          class="p-2.5 rounded-xl text-white/90 hover:text-white hover:bg-white/20 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
          title="导出图像">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- 退出纯净模式按钮 -->
    <button
      v-if="isPureMode"
      @click="togglePureMode"
      class="absolute top-6 right-6 z-20 p-3 smart-toolbar rounded-full text-white hover:bg-white/10 transition-colors shadow-2xl">
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
      </svg>
    </button>

  </main>
</template>

<script setup>
import { useGradient } from '@/composables/useGradient'

const {
  previewMode,
  previewStyle,
  generatedImage,
  isGenerating,
  loadingText,
  loadingProgress,
  isPureMode,
  generateGradient,
  copyCSS,
  exportImage,
  randomGradient,
  toggleFullscreen
} = useGradient()

function togglePureMode() {
  isPureMode.value = !isPureMode.value
  toggleFullscreen()
}
</script>
