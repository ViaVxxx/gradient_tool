<template>
  <div class="min-h-screen bg-gradient-to-br from-gray-50 via-white to-blue-50">
    <!-- 现代化头部 -->
    <header class="bg-white/80 backdrop-blur-xl border-b border-gray-200/50 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg">
              <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent">
                Gradient Studio
              </h1>
              <p class="text-sm text-gray-500">专业渐变设计工具</p>
            </div>
          </div>

          <!-- 快捷操作栏 -->
          <div class="flex items-center space-x-3">
            <button @click="randomGradient"
                    class="px-4 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium transition-all duration-200 flex items-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              <span>随机生成</span>
            </button>
            
            <button @click="exportImage"
                    :disabled="!generatedImage"
                    class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-300 text-white text-sm font-medium transition-all duration-200 flex items-center space-x-2">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
              <span>导出</span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="max-w-7xl mx-auto px-6 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">

        <!-- 左栏：渐变设计控制 -->
        <div class="lg:col-span-3 space-y-6" :class="{ 'disable-blur': isDragging }">

          <!-- 渐变类型卡片 -->
          <div class="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/20 p-6 shadow-xl shadow-gray-200/50">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
              </svg>
              渐变类型
            </h3>
            <div class="grid grid-cols-1 gap-3">
              <button
                v-for="type in gradientTypes"
                :key="type.value"
                @click="gradientType = type.value"
                :class="[
                  'px-4 py-3 rounded-xl text-sm font-medium transition-all duration-200 flex items-center justify-center space-x-2',
                  gradientType === type.value
                    ? 'bg-gradient-to-r from-indigo-500 to-purple-600 text-white shadow-lg shadow-indigo-500/30'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]">
                <component :is="type.icon" class="w-4 h-4" />
                <span>{{ type.label }}</span>
              </button>
            </div>
          </div>

          <!-- 增强版色标编辑器 -->
          <div class="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/20 p-6 shadow-xl shadow-gray-200/50">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold text-gray-800 flex items-center">
                <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                </svg>
                色标编辑
              </h3>
              <div class="flex items-center gap-2">
                <span class="text-xs text-gray-500">{{ colorStops.length }}/20</span>
                <button @click="addColorStop"
                        :disabled="colorStops.length >= 20"
                        class="px-3 py-1.5 rounded-lg text-xs bg-indigo-50 text-indigo-600 hover:bg-indigo-100 disabled:opacity-50 transition-colors">
                  + 添加
                </button>
              </div>
            </div>

            <!-- 增强版渐变条 -->
            <div class="relative mb-6">
              <!-- 渐变条背景 -->
              <div 
                class="relative h-16 rounded-xl border-2 border-gray-300 overflow-hidden cursor-crosshair shadow-inner"
                :style="previewStyle"
                @click="addColorStopAtPosition">
                
                <!-- 网格线 -->
                <div class="absolute inset-0 opacity-20">
                  <div v-for="i in 4" :key="i" 
                       class="absolute top-0 bottom-0 w-px bg-white"
                       :style="{ left: (i * 25) + '%' }"></div>
                </div>
                
                <!-- 色标指示器 -->
                <div 
                  v-for="(stop, index) in colorStops" 
                  :key="index"
                  class="absolute top-0 transform -translate-x-1/2 cursor-pointer group z-10"
                  :style="{ left: (stop.position * 100) + '%' }"
                  @mousedown="startDragColorStop(index, $event)"
                  @click.stop="selectedColorStopIndex = index">
                  
                  <!-- 色标手柄 -->
                  <div class="relative">
                    <!-- 连接线 -->
                    <div class="w-1 h-16 bg-white/80 shadow-sm mx-auto"></div>
                    
                    <!-- 圆形手柄 -->
                    <div 
                      :class="[
                        'absolute -top-2 left-1/2 transform -translate-x-1/2 w-8 h-8 rounded-full border-3 shadow-lg transition-all duration-200',
                        selectedColorStopIndex === index 
                          ? 'border-indigo-500 scale-110 shadow-indigo-500/30' 
                          : 'border-white group-hover:scale-105'
                      ]"
                      :style="{ backgroundColor: stop.hex }">
                    </div>
                    
                    <!-- 位置标签 -->
                    <div class="absolute -bottom-6 left-1/2 transform -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <span class="text-xs bg-gray-900 text-white px-2 py-1 rounded whitespace-nowrap">
                        {{ Math.round(stop.position * 100) }}%
                      </span>
                    </div>
                    
                    <!-- 删除按钮 -->
                    <button 
                      v-if="colorStops.length > 2"
                      @click.stop="removeColorStop(index)"
                      class="absolute -top-1 -right-1 w-5 h-5 bg-red-500 text-white rounded-full text-xs opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center hover:bg-red-600">
                      ×
                    </button>
                  </div>
                </div>
              </div>

              <!-- 位置标尺 -->
              <div class="flex justify-between text-xs text-gray-400 mt-2 px-4">
                <span>0%</span>
                <span>25%</span>
                <span>50%</span>
                <span>75%</span>
                <span>100%</span>
              </div>
            </div>

            <!-- 当前选中色标的详细编辑 -->
            <div v-if="selectedColorStopIndex !== null" class="space-y-4 p-5 bg-gradient-to-br from-gray-50 to-gray-100 rounded-xl border border-gray-200">
              <div class="flex items-center justify-between">
                <h4 class="text-sm font-semibold text-gray-700">编辑色标 #{{ selectedColorStopIndex + 1 }}</h4>
                <span class="text-xs text-gray-500 font-mono">{{ Math.round(colorStops[selectedColorStopIndex].position * 100) }}%</span>
              </div>

              <div class="grid grid-cols-2 gap-4">
                <!-- 颜色选择器 -->
                <div>
                  <label class="block text-xs font-medium text-gray-600 mb-2">颜色选择</label>
                  <div class="relative">
                    <!-- 大色块显示 -->
                    <div 
                      class="w-full h-24 rounded-xl border-2 border-gray-200 cursor-pointer relative overflow-hidden shadow-inner hover:shadow-lg transition-shadow"
                      :style="{ backgroundColor: colorStops[selectedColorStopIndex].hex }"
                      @click="$refs.colorPicker.click()">
                      
                      <!-- 隐藏的颜色输入 -->
                      <input
                        ref="colorPicker"
                        type="color"
                        v-model="colorStops[selectedColorStopIndex].hex"
                        @change="updateColorFromHex(selectedColorStopIndex)"
                        class="absolute inset-0 w-full h-full opacity-0 cursor-pointer">
                      
                      <!-- 选择指示器 -->
                      <div class="absolute inset-0 flex items-center justify-center">
                        <div class="w-10 h-10 rounded-full border-2 border-white/60 flex items-center justify-center backdrop-blur-sm">
                          <svg class="w-5 h-5 text-white/80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                          </svg>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 数值输入区域 -->
                <div class="space-y-3">
                  <!-- HEX 输入 -->
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">HEX</label>
                    <input
                      type="text"
                      v-model="colorStops[selectedColorStopIndex].hex"
                      @input="updateColorFromHex(selectedColorStopIndex)"
                      class="w-full px-3 py-2 border border-gray-300 rounded-lg text-sm font-mono bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      placeholder="#8FCF72">
                  </div>

                  <!-- RGB 输入 -->
                  <div>
                    <label class="block text-xs font-medium text-gray-600 mb-1">RGB</label>
                    <div class="grid grid-cols-3 gap-1">
                      <input
                        type="number"
                        v-model.number="colorStops[selectedColorStopIndex].color.r"
                        @input="updateHexFromRgb(selectedColorStopIndex)"
                        min="0" max="255"
                        class="px-2 py-1 border border-gray-300 rounded text-xs text-center bg-white focus:ring-1 focus:ring-indigo-500">
                      <input
                        type="number"
                        v-model.number="colorStops[selectedColorStopIndex].color.g"
                        @input="updateHexFromRgb(selectedColorStopIndex)"
                        min="0" max="255"
                        class="px-2 py-1 border border-gray-300 rounded text-xs text-center bg-white focus:ring-1 focus:ring-indigo-500">
                      <input
                        type="number"
                        v-model.number="colorStops[selectedColorStopIndex].color.b"
                        @input="updateHexFromRgb(selectedColorStopIndex)"
                        min="0" max="255"
                        class="px-2 py-1 border border-gray-300 rounded text-xs text-center bg-white focus:ring-1 focus:ring-indigo-500">
                    </div>
                    <div class="grid grid-cols-3 gap-1 mt-1">
                      <span class="text-xs text-gray-400 text-center">R</span>
                      <span class="text-xs text-gray-400 text-center">G</span>
                      <span class="text-xs text-gray-400 text-center">B</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- 位置调整 -->
              <div>
                <label class="block text-xs font-medium text-gray-600 mb-2">位置调整</label>
                <div class="flex items-center gap-3">
                  <input
                    type="range"
                    v-model.number="colorStops[selectedColorStopIndex].position"
                    min="0" max="1" step="0.01"
                    class="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider">
                  <input
                    type="number"
                    v-model.number="colorStops[selectedColorStopIndex].position"
                    min="0" max="1" step="0.01"
                    class="w-20 px-2 py-1 border border-gray-300 rounded text-xs text-center font-mono bg-white focus:ring-1 focus:ring-indigo-500">
                </div>
              </div>
            </div>
          </div>

          <!-- 角度控制（仅线性渐变） -->
          <div v-if="gradientType === 'linear'"
               class="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/20 p-6 shadow-xl shadow-gray-200/50">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              角度控制
            </h3>
            
            <div class="flex items-center gap-6">
              <!-- 增强版圆盘选择器 -->
              <div class="relative w-32 h-32">
                <svg class="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                  <!-- 外圈背景 -->
                  <circle cx="50" cy="50" r="45" fill="none" stroke="#E5E7EB" stroke-width="2"/>
                  <!-- 刻度线 -->
                  <g stroke="#9CA3AF" stroke-width="1">
                    <line v-for="i in 12" :key="i" 
                          :x1="50 + 40 * Math.cos((i * 30) * Math.PI / 180)" 
                          :y1="50 + 40 * Math.sin((i * 30) * Math.PI / 180)"
                          :x2="50 + 45 * Math.cos((i * 30) * Math.PI / 180)" 
                          :y2="50 + 45 * Math.sin((i * 30) * Math.PI / 180)"/>
                  </g>
                  <!-- 渐变指针 -->
                  <defs>
                    <linearGradient id="pointerGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                      <stop offset="0%" style="stop-color:#6366F1"/>
                      <stop offset="100%" style="stop-color:#8B5CF6"/>
                    </linearGradient>
                  </defs>
                  <line
                    :x1="50"
                    :y1="50"
                    :x2="50 + 35 * Math.cos(angle * Math.PI / 180)"
                    :y2="50 + 35 * Math.sin(angle * Math.PI / 180)"
                    stroke="url(#pointerGradient)"
                    stroke-width="3"
                    stroke-linecap="round"/>
                  <!-- 中心点 -->
                  <circle cx="50" cy="50" r="5" fill="url(#pointerGradient)" stroke="white" stroke-width="2"/>
                </svg>
                <!-- 交互层 -->
                <div
                  class="absolute inset-0 cursor-pointer"
                  @mousedown="startAngleDrag"
                  @touchstart="startAngleDrag">
                </div>
              </div>

              <!-- 数字输入和快捷按钮 -->
              <div class="flex-1 space-y-4">
                <div>
                  <input
                    type="number"
                    v-model.number="angle"
                    min="0"
                    max="360"
                    step="1"
                    class="w-full px-4 py-3 border border-gray-300 rounded-xl text-center text-2xl font-bold text-indigo-600 bg-white focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500">
                  <div class="text-xs text-gray-500 text-center mt-1">度 (°)</div>
                </div>
                
                <!-- 快捷角度按钮 -->
                <div class="grid grid-cols-4 gap-2">
                  <button
                    v-for="quickAngle in [0, 45, 90, 135, 180, 225, 270, 315]"
                    :key="quickAngle"
                    @click="angle = quickAngle"
                    :class="[
                      'px-2 py-1 rounded-lg text-xs font-medium transition-colors',
                      angle === quickAngle 
                        ? 'bg-indigo-600 text-white' 
                        : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                    ]">
                    {{ quickAngle }}°
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- 中栏：预览区域 -->
        <div class="lg:col-span-6">
          <div class="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/20 p-6 shadow-xl shadow-gray-200/50 h-full">
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold text-gray-800 flex items-center">
                <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
                实时预览
              </h3>
              <div class="flex items-center gap-4">
                <div class="flex items-center gap-2 text-xs text-gray-500">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span class="font-mono">800 × 600</span>
                </div>
                
                <!-- 预览模式切换 -->
                <div class="flex items-center bg-gray-100 rounded-lg p-1">
                  <button
                    @click="previewMode = 'css'"
                    :class="[
                      'px-3 py-1 rounded text-xs font-medium transition-colors',
                      previewMode === 'css' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600'
                    ]">
                    CSS
                  </button>
                  <button
                    @click="previewMode = 'image'"
                    :class="[
                      'px-3 py-1 rounded text-xs font-medium transition-colors',
                      previewMode === 'image' ? 'bg-white text-gray-900 shadow-sm' : 'text-gray-600'
                    ]">
                    图像
                  </button>
                </div>
              </div>
            </div>

            <!-- 渐变预览画布 -->
            <div class="relative rounded-xl overflow-hidden border-2 border-gray-200 shadow-inner" style="aspect-ratio: 4/3;">
              <!-- CSS 预览模式 -->
              <div
                v-if="previewMode === 'css' || !generatedImage"
                class="absolute inset-0 flex items-center justify-center"
                :style="previewStyle">
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

              <!-- 生成图像预览 -->
              <img
                v-if="previewMode === 'image' && generatedImage"
                :src="generatedImage"
                alt="Generated gradient"
                class="absolute inset-0 w-full h-full object-cover">

              <!-- 生成中加载状态 -->
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

              <!-- 预览工具栏 -->
              <div class="absolute top-4 right-4 flex items-center gap-2">
                <button
                  v-if="generatedImage"
                  @click="toggleFullscreen"
                  class="p-2 bg-black/20 backdrop-blur-sm rounded-lg text-white/80 hover:text-white hover:bg-black/30 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                  </svg>
                </button>
              </div>
            </div>

            <!-- 操作按钮区域 -->
            <div class="mt-6 space-y-3">
              <button @click="generateGradient"
                      :disabled="isGenerating"
                      class="w-full px-6 py-4 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white text-lg font-semibold transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-indigo-500/30 hover:shadow-xl hover:shadow-indigo-500/40">
                <span class="flex items-center justify-center gap-3">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span>{{ isGenerating ? loadingText : '生成渐变图像' }}</span>
                </span>
              </button>
              
              <!-- 快捷操作 -->
              <div class="grid grid-cols-2 gap-3">
                <button @click="copyCSS"
                        class="px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium transition-colors flex items-center justify-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                  </svg>
                  <span>复制 CSS</span>
                </button>
                
                <button @click="savePreset"
                        :disabled="!generatedImage"
                        class="px-4 py-2 rounded-lg bg-gray-100 hover:bg-gray-200 disabled:bg-gray-50 disabled:text-gray-400 text-gray-700 text-sm font-medium transition-colors flex items-center justify-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                  <span>收藏</span>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 右栏：效果和预设 -->
        <div class="lg:col-span-3 space-y-6">

          <!-- 纹理效果面板 -->
          <div class="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/20 p-6 shadow-xl shadow-gray-200/50">
            <h3 class="text-lg font-semibold text-gray-800 mb-4 flex items-center">
              <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
              纹理效果
            </h3>
            
            <div class="space-y-4">
              <div
                v-for="effect in effects"
                :key="effect.value"
                class="relative overflow-hidden rounded-xl border-2 transition-all duration-200"
                :class="effectsEnabled[effect.value] ? 'border-indigo-300 bg-indigo-50/50' : 'border-gray-200 bg-gray-50/50'">

                <!-- 效果预览缩略图 -->
                <div class="h-20 relative overflow-hidden">
                  <div 
                    class="absolute inset-0 opacity-30"
                    :style="getEffectPreviewStyle(effect.value)">
                  </div>
                  <div class="absolute inset-0 flex items-center justify-center">
                    <div class="text-center">
                      <div class="text-2xl mb-1">{{ effect.icon }}</div>
                      <div class="text-xs font-medium text-gray-700">{{ effect.label }}</div>
                    </div>
                  </div>
                </div>

                <!-- 效果控制 -->
                <div class="p-4">
                  <div class="flex items-center justify-between mb-3">
                    <label class="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        v-model="effectsEnabled[effect.value]"
                        @change="toggleEffect(effect.value)"
                        class="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                      <span class="text-sm font-medium" :class="effectsEnabled[effect.value] ? 'text-gray-900' : 'text-gray-500'">
                        启用效果
                      </span>
                    </label>
                    <span v-if="effectsEnabled[effect.value]" class="text-xs font-mono font-semibold text-indigo-600">
                      {{ Math.round(effectIntensities[effect.value] * 100) }}%
                    </span>
                  </div>

                  <!-- 强度滑块 -->
                  <div v-if="effectsEnabled[effect.value]" class="space-y-2">
                    <div class="flex items-center justify-between text-xs text-gray-500">
                      <span>强度</span>
                      <span>{{ effect.description }}</span>
                    </div>
                    <input
                      type="range"
                      v-model.number="effectIntensities[effect.value]"
                      min="0.05"
                      max="1"
                      step="0.05"
                      class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider">
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- 预设库 -->
          <div class="bg-white/70 backdrop-blur-xl rounded-2xl border border-white/20 p-6 shadow-xl shadow-gray-200/50">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-lg font-semibold text-gray-800 flex items-center">
                <svg class="w-5 h-5 mr-2 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
                </svg>
                预设库
              </h3>
              
              <!-- 预设分类筛选 -->
              <select v-model="selectedPresetCategory" 
                      class="text-xs border border-gray-300 rounded-lg px-2 py-1 bg-white focus:ring-1 focus:ring-indigo-500">
                <option value="">全部</option>
                <option value="nature">自然</option>
                <option value="sunset">日落</option>
                <option value="ocean">海洋</option>
                <option value="abstract">抽象</option>
              </select>
            </div>
            
            <div class="grid grid-cols-2 gap-3 max-h-96 overflow-y-auto custom-scrollbar">
              <button
                v-for="preset in filteredPresets"
                :key="preset.name"
                @click="loadPreset(preset)"
                class="group relative h-20 rounded-xl overflow-hidden border-2 border-gray-200 hover:border-indigo-300 transition-all duration-200 shadow-sm hover:shadow-md">
                
                <!-- 预设预览 -->
                <div
                  class="absolute inset-0"
                  :style="getPresetStyle(preset)">
                </div>
                
                <!-- 悬停信息 -->
                <div class="absolute inset-0 bg-gradient-to-t from-black/70 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-3">
                  <div class="text-left">
                    <div class="text-xs text-white font-semibold truncate">{{ preset.name }}</div>
                    <div class="text-xs text-white/80">{{ preset.category }}</div>
                  </div>
                </div>
                
                <!-- 选中指示器 -->
                <div class="absolute top-2 right-2 w-6 h-6 rounded-full bg-white/20 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                  <svg class="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 全屏预览模态框 -->
    <div v-if="isFullscreen" 
         class="fixed inset-0 bg-black/90 backdrop-blur-sm z-50 flex items-center justify-center p-4"
         @click="toggleFullscreen">
      <div class="relative max-w-4xl max-h-full">
        <img :src="generatedImage" alt="Full screen preview" class="max-w-full max-h-full object-contain rounded-lg shadow-2xl">
        <button @click="toggleFullscreen" 
                class="absolute top-4 right-4 p-2 bg-black/50 backdrop-blur-sm rounded-lg text-white hover:bg-black/70 transition-colors">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, reactive, computed, watch, onMounted, h } from 'vue'
import { api, preloadWasm } from '@/api'

// 响应式数据
const gradientType = ref('linear')
const angle = ref(90)
const colorStops = ref([
  { position: 0, color: { r: 42, g: 123, b: 155 }, hex: '#2A7B9B', alpha: 100 },
  { position: 0.4, color: { r: 87, g: 199, b: 133 }, hex: '#57C785', alpha: 100 },
  { position: 0.62, color: { r: 143, g: 207, b: 114 }, hex: '#8FCF72', alpha: 100 },
  { position: 1, color: { r: 237, g: 221, b: 83 }, hex: '#EDDD53', alpha: 100 }
])
const selectedColorStopIndex = ref(0)
const generatedImage = ref(null)
const originalImage = ref(null)
const isGenerating = ref(false)
const loadingText = ref('生成中...')
const loadingProgress = ref(0)
const presets = ref([])
const apiReady = ref(false)
const lastAppliedEffect = ref(null)
const previewMode = ref('css')
const isFullscreen = ref(false)
const selectedPresetCategory = ref('')
const isDragging = ref(false) // 拖拽状态标记

// 效果状态
const effectsEnabled = ref({
  perlin: false,
  frosted: false,
  film: false,
  vignette: false
})

const effectIntensities = ref({
  perlin: 0.3,
  frosted: 0.2,
  film: 0.25,
  vignette: 0.5
})

// 渐变类型选项（带图标组件）
const gradientTypes = [
  { 
    label: '线性渐变', 
    value: 'linear',
    icon: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 7h8m0 0v8m0-8l-8 8-4-4-6 6' })
    ])
  },
  { 
    label: '径向渐变', 
    value: 'radial',
    icon: () => h('svg', { class: 'w-4 h-4', fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M21 12a9 9 0 11-18 0 9 9 0 0118 0z' }),
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12a3 3 0 106 0 3 3 0 00-6 0z' })
    ])
  }
]

// 纹理效果选项
const effects = [
  { 
    label: 'Perlin 噪点', 
    value: 'perlin', 
    icon: '✨',
    description: '自然纹理质感'
  },
  { 
    label: '磨砂玻璃', 
    value: 'frosted', 
    icon: '🌫️',
    description: '毛玻璃模糊效果'
  },
  { 
    label: '胶片颗粒', 
    value: 'film', 
    icon: '🎞️',
    description: '复古胶片质感'
  },
  { 
    label: '晕影效果', 
    value: 'vignette', 
    icon: '🎭',
    description: '边缘暗角效果'
  }
]

// 等待 API 准备好（WASM + Tauri）
async function waitForAPI() {
  try {
    await preloadWasm()
    apiReady.value = true
    console.log('✓ WASM + Tauri API 已准备好')
    return true
  } catch (error) {
    console.error('✗ API 初始化失败:', error)
    return false
  }
}

// 实时预览样式
const previewStyle = computed(() => {
  const stops = colorStops.value.map(stop => {
    const { r, g, b } = stop.color
    return `rgb(${r},${g},${b}) ${stop.position * 100}%`
  }).join(', ')

  if (gradientType.value === 'linear') {
    return {
      background: `linear-gradient(${angle.value}deg, ${stops})`
    }
  } else {
    return {
      background: `radial-gradient(circle, ${stops})`
    }
  }
})

// 筛选后的预设
const filteredPresets = computed(() => {
  if (!selectedPresetCategory.value) return presets.value
  return presets.value.filter(preset => preset.category === selectedPresetCategory.value)
})

// 颜色转换辅助函数
function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null
}

function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map(x => {
    const hex = x.toString(16)
    return hex.length === 1 ? '0' + hex : hex
  }).join('')
}

// 更新颜色
function updateColorFromHex(index) {
  const rgb = hexToRgb(colorStops.value[index].hex)
  if (rgb) {
    colorStops.value[index].color = rgb
  }
}

function updateHexFromRgb(index) {
  const stop = colorStops.value[index]
  stop.hex = rgbToHex(stop.color.r, stop.color.g, stop.color.b)
}

// 在指定位置添加色标
function addColorStopAtPosition(event) {
  if (colorStops.value.length >= 20) return
  
  const rect = event.currentTarget.getBoundingClientRect()
  const x = event.clientX - rect.left
  const position = Math.max(0, Math.min(1, x / rect.width))
  
  const interpolatedColor = interpolateColorAtPosition(position)
  
  const newStop = {
    position: Math.round(position * 100) / 100,
    color: interpolatedColor,
    hex: rgbToHex(interpolatedColor.r, interpolatedColor.g, interpolatedColor.b),
    alpha: 100
  }
  
  let insertIndex = colorStops.value.findIndex(stop => stop.position > position)
  if (insertIndex === -1) insertIndex = colorStops.value.length
  
  colorStops.value.splice(insertIndex, 0, newStop)
  selectedColorStopIndex.value = insertIndex
}

// 在指定位置插值颜色
function interpolateColorAtPosition(position) {
  const stops = [...colorStops.value].sort((a, b) => a.position - b.position)
  
  let leftStop = stops[0]
  let rightStop = stops[stops.length - 1]
  
  for (let i = 0; i < stops.length - 1; i++) {
    if (position >= stops[i].position && position <= stops[i + 1].position) {
      leftStop = stops[i]
      rightStop = stops[i + 1]
      break
    }
  }
  
  if (position <= leftStop.position) return { ...leftStop.color }
  if (position >= rightStop.position) return { ...rightStop.color }
  
  const t = (position - leftStop.position) / (rightStop.position - leftStop.position)
  
  return {
    r: Math.round(leftStop.color.r + (rightStop.color.r - leftStop.color.r) * t),
    g: Math.round(leftStop.color.g + (rightStop.color.g - leftStop.color.g) * t),
    b: Math.round(leftStop.color.b + (rightStop.color.b - leftStop.color.b) * t)
  }
}

// 开始拖拽色标
function startDragColorStop(index, event) {
  event.preventDefault()
  selectedColorStopIndex.value = index
  isDragging.value = true

  const gradientBar = event.currentTarget.closest('.relative')
  const rect = gradientBar.getBoundingClientRect()

  let rafId = null

  const updatePosition = (clientX) => {
    const x = clientX - rect.left
    const position = Math.max(0, Math.min(1, x / rect.width))
    colorStops.value[index].position = Math.round(position * 100) / 100
  }

  const handleMove = (e) => {
    if (rafId) return
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    rafId = requestAnimationFrame(() => {
      updatePosition(clientX)
      rafId = null
    })
  }

  const handleEnd = () => {
    if (rafId) {
      cancelAnimationFrame(rafId)
      rafId = null
    }
    isDragging.value = false
    document.removeEventListener('mousemove', handleMove)
    document.removeEventListener('mouseup', handleEnd)
    document.removeEventListener('touchmove', handleMove)
    document.removeEventListener('touchend', handleEnd)
  }

  document.addEventListener('mousemove', handleMove)
  document.addEventListener('mouseup', handleEnd)
  document.addEventListener('touchmove', handleMove)
  document.addEventListener('touchend', handleEnd)
}

// 色标管理
function addColorStop() {
  if (colorStops.value.length >= 20) return
  
  const newPosition = 0.5
  const interpolatedColor = interpolateColorAtPosition(newPosition)
  
  const newStop = {
    position: newPosition,
    color: interpolatedColor,
    hex: rgbToHex(interpolatedColor.r, interpolatedColor.g, interpolatedColor.b),
    alpha: 100
  }
  
  colorStops.value.push(newStop)
  selectedColorStopIndex.value = colorStops.value.length - 1
}

function removeColorStop(index) {
  if (colorStops.value.length <= 2) return
  
  colorStops.value.splice(index, 1)
  
  if (selectedColorStopIndex.value >= colorStops.value.length) {
    selectedColorStopIndex.value = colorStops.value.length - 1
  } else if (selectedColorStopIndex.value === index && index > 0) {
    selectedColorStopIndex.value = index - 1
  }
}

// 角度拖动
function startAngleDrag(e) {
  e.preventDefault()
  isDragging.value = true

  let rafId = null

  const updateAngle = (clientX, clientY) => {
    const target = e.currentTarget
    const rect = target.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2

    const deltaX = clientX - centerX
    const deltaY = clientY - centerY

    let newAngle = Math.atan2(deltaY, deltaX) * 180 / Math.PI
    if (newAngle < 0) newAngle += 360

    angle.value = Math.round(newAngle)
  }

  const handleMove = (e) => {
    if (rafId) return
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    const clientY = e.touches ? e.touches[0].clientY : e.clientY
    rafId = requestAnimationFrame(() => {
      updateAngle(clientX, clientY)
      rafId = null
    })
  }

  const handleEnd = () => {
    if (rafId) {
      cancelAnimationFrame(rafId)
      rafId = null
    }
    isDragging.value = false
    document.removeEventListener('mousemove', handleMove)
    document.removeEventListener('mouseup', handleEnd)
    document.removeEventListener('touchmove', handleMove)
    document.removeEventListener('touchend', handleEnd)
  }

  document.addEventListener('mousemove', handleMove)
  document.addEventListener('mouseup', handleEnd)
  document.addEventListener('touchmove', handleMove)
  document.addEventListener('touchend', handleEnd)

  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY
  updateAngle(clientX, clientY)
}

// 切换效果
function toggleEffect(effectType) {
  if (effectsEnabled.value[effectType]) {
    if (effectIntensities.value[effectType] < 0.1) {
      effectIntensities.value[effectType] = 0.3
    }
    applyEffect(effectType)
  } else {
    if (originalImage.value) {
      generatedImage.value = originalImage.value
      lastAppliedEffect.value = null
    }
  }
}

// 生成渐变
async function generateGradient() {
  if (!apiReady.value) {
    await waitForAPI()
  }

  isGenerating.value = true
  loadingText.value = '正在生成渐变...'
  loadingProgress.value = 0
  
  // 模拟进度
  const progressInterval = setInterval(() => {
    if (loadingProgress.value < 90) {
      loadingProgress.value += Math.random() * 20
    }
  }, 200)

  try {
    const result = await api.generate_gradient(
      gradientType.value,
      colorStops.value,
      angle.value
    )

    clearInterval(progressInterval)
    loadingProgress.value = 100

    if (result.success) {
      generatedImage.value = result.image
      originalImage.value = result.image

      // 保存到全局状态供 API 使用
      window.__currentGradientImage__ = result.image

      lastAppliedEffect.value = null
      previewMode.value = 'image'
    } else {
      alert('生成失败: ' + result.error)
    }
  } catch (error) {
    clearInterval(progressInterval)
    console.error('生成错误:', error)
    alert('生成失败: ' + error.message)
  } finally {
    isGenerating.value = false
    loadingProgress.value = 0
  }
}

// 应用效果
async function applyEffect(effectType, intensity = null) {
  if (!apiReady.value) {
    await waitForAPI()
  }

  if (!originalImage.value) {
    await generateGradient()
  }

  lastAppliedEffect.value = effectType
  isGenerating.value = true
  loadingText.value = `正在应用${effects.find(e => e.value === effectType)?.label}...`

  try {
    const effectIntensity = intensity !== null ? intensity : effectIntensities.value[effectType]
    const result = await api.apply_effect(effectType, effectIntensity)

    if (result.success) {
      generatedImage.value = result.image

      // 更新全局状态
      window.__currentGradientImage__ = result.image

      previewMode.value = 'image'
    } else {
      alert('应用效果失败: ' + result.error)
    }
  } catch (error) {
    console.error('效果错误:', error)
    alert('应用效果失败: ' + error.message)
  } finally {
    isGenerating.value = false
  }
}

// 随机生成
function randomGradient() {
  const count = Math.floor(Math.random() * 3) + 2
  colorStops.value = []

  for (let i = 0; i < count; i++) {
    const r = Math.floor(Math.random() * 256)
    const g = Math.floor(Math.random() * 256)
    const b = Math.floor(Math.random() * 256)

    colorStops.value.push({
      position: i / (count - 1),
      color: { r, g, b },
      hex: rgbToHex(r, g, b),
      alpha: 100
    })
  }

  selectedColorStopIndex.value = 0
  angle.value = Math.floor(Math.random() * 360)
  generateGradient()
}

// 导出图像
async function exportImage() {
  if (!apiReady.value) {
    await waitForAPI()
  }

  if (!generatedImage.value) {
    alert('请先生成渐变')
    return
  }

  try {
    const result = await api.export_image('png', 95)

    if (result.success) {
      alert('导出成功: ' + result.filepath)
    } else {
      alert('导出失败: ' + result.error)
    }
  } catch (error) {
    console.error('导出错误:', error)
    alert('导出失败: ' + error.message)
  }
}

// 复制CSS
function copyCSS() {
  const stops = colorStops.value.map(stop => {
    const { r, g, b } = stop.color
    return `rgb(${r},${g},${b}) ${stop.position * 100}%`
  }).join(', ')

  let cssText = ''
  if (gradientType.value === 'linear') {
    cssText = `background: linear-gradient(${angle.value}deg, ${stops});`
  } else {
    cssText = `background: radial-gradient(circle, ${stops});`
  }

  navigator.clipboard.writeText(cssText).then(() => {
    alert('CSS 代码已复制到剪贴板')
  }).catch(() => {
    alert('复制失败，请手动复制')
  })
}

// 保存预设
function savePreset() {
  const name = prompt('请输入预设名称:')
  if (!name) return

  // 这里可以调用API保存预设
  alert('预设保存功能待实现')
}

// 加载预设
function loadPreset(preset) {
  gradientType.value = preset.gradient_type
  angle.value = preset.angle || 90

  colorStops.value = preset.stops.map(stop => ({
    position: stop.position,
    color: stop.color,
    hex: rgbToHex(stop.color.r, stop.color.g, stop.color.b),
    alpha: 100
  }))

  selectedColorStopIndex.value = 0
  generateGradient()
}

// 获取预设样式
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

// 获取效果预览样式
function getEffectPreviewStyle(effectType) {
  const baseGradient = 'linear-gradient(45deg, #667eea 0%, #764ba2 100%)'
  
  switch (effectType) {
    case 'perlin':
      return { 
        background: baseGradient,
        filter: 'contrast(1.2) brightness(0.9)'
      }
    case 'frosted':
      return { 
        background: baseGradient,
        filter: 'blur(1px) brightness(1.1)'
      }
    case 'film':
      return { 
        background: baseGradient,
        filter: 'sepia(0.3) contrast(1.1)'
      }
    case 'vignette':
      return { 
        background: `radial-gradient(circle, transparent 30%, rgba(0,0,0,0.3) 100%), ${baseGradient}`
      }
    default:
      return { background: baseGradient }
  }
}

// 切换全屏
function toggleFullscreen() {
  isFullscreen.value = !isFullscreen.value
}

// 加载预设列表
async function loadPresets() {
  if (!apiReady.value) {
    await waitForAPI()
  }

  try {
    presets.value = await api.get_presets()
  } catch (error) {
    console.error('加载预设失败:', error)
  }
}

// 组件挂载
onMounted(async () => {
  await waitForAPI()
  await loadPresets()
  await generateGradient()
})

// 监听变化
watch([gradientType, angle, colorStops], () => {
  // 实时预览会自动更新
}, { deep: true })

// 监听效果强度变化
let debounceTimer = null
watch(effectIntensities, () => {
  if (!lastAppliedEffect.value || !originalImage.value || !effectsEnabled.value[lastAppliedEffect.value]) return

  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }

  debounceTimer = setTimeout(() => {
    if (!isGenerating.value) {
      applyEffect(lastAppliedEffect.value)
    }
  }, 500)
}, { deep: true })
</script>
<style scoped>
/* 自定义滑块样式 */
.slider::-webkit-slider-thumb {
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  cursor: pointer;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
  transition: all 0.2s ease;
  border: 2px solid white;
}

.slider::-webkit-slider-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.6);
}

.slider::-webkit-slider-thumb:active {
  transform: scale(1.1);
}

.slider::-moz-range-thumb {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366F1, #8B5CF6);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.4);
  transition: all 0.2s ease;
}

.slider::-moz-range-thumb:hover {
  transform: scale(1.15);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.6);
}

.slider::-webkit-slider-track {
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(90deg, #E5E7EB, #D1D5DB);
}

.slider::-moz-range-track {
  height: 6px;
  border-radius: 3px;
  background: linear-gradient(90deg, #E5E7EB, #D1D5DB);
  border: none;
}

/* 自定义滚动条 */
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: rgba(243, 244, 246, 0.5);
  border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #D1D5DB, #9CA3AF);
  border-radius: 3px;
  transition: background 0.2s ease;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #9CA3AF, #6B7280);
}

/* 玻璃态效果增强 */
.backdrop-blur-xl {
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
}

/* 动画效果 */
@keyframes pulse-glow {
  0%, 100% {
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
  }
  50% {
    box-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
  }
}

.animate-pulse-glow {
  animation: pulse-glow 2s ease-in-out infinite;
}

/* 渐变条增强效果 */
.gradient-bar-enhanced {
  position: relative;
  overflow: hidden;
}

.gradient-bar-enhanced::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
  animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
  0% { left: -100%; }
  100% { left: 100%; }
}

/* 色标手柄增强 */
.color-stop-handle {
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

.color-stop-handle:hover {
  transform: scale(1.1);
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.2));
}

.color-stop-handle.selected {
  transform: scale(1.15);
  filter: drop-shadow(0 6px 12px rgba(99, 102, 241, 0.4));
}

/* 按钮增强效果 */
.btn-enhanced {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.btn-enhanced::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
  transition: left 0.5s ease;
}

.btn-enhanced:hover::before {
  left: 100%;
}

/* 卡片悬停效果 */
.card-hover {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.card-hover:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
}

/* 预设缩略图增强 */
.preset-thumbnail {
  position: relative;
  overflow: hidden;
  transition: all 0.3s ease;
}

.preset-thumbnail::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(45deg, transparent 30%, rgba(255, 255, 255, 0.1) 50%, transparent 70%);
  transform: translateX(-100%);
  transition: transform 0.6s ease;
}

.preset-thumbnail:hover::after {
  transform: translateX(100%);
}

/* 加载动画增强 */
@keyframes spin-glow {
  0% {
    transform: rotate(0deg);
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
  }
  50% {
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.6);
  }
  100% {
    transform: rotate(360deg);
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.3);
  }
}

.loading-spinner {
  animation: spin-glow 1s linear infinite;
}

/* 响应式优化 */
@media (max-width: 1024px) {
  .lg\:col-span-3,
  .lg\:col-span-6 {
    grid-column: span 12;
  }
  
  .grid.grid-cols-1.lg\:grid-cols-12 {
    gap: 1.5rem;
  }
}

@media (max-width: 640px) {
  .grid.grid-cols-2 {
    grid-template-columns: 1fr;
  }
  
  .px-6 {
    padding-left: 1rem;
    padding-right: 1rem;
  }
}

/* 深色模式支持 */
@media (prefers-color-scheme: dark) {
  .bg-white\/70 {
    background-color: rgba(31, 41, 55, 0.8);
  }
  
  .text-gray-800 {
    color: rgb(229, 231, 235);
  }
  
  .text-gray-700 {
    color: rgb(209, 213, 219);
  }
  
  .border-white\/20 {
    border-color: rgba(75, 85, 99, 0.3);
  }
}

/* 无障碍优化 */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* 高对比度模式 */
@media (prefers-contrast: high) {
  .border-gray-200 {
    border-color: rgb(0, 0, 0);
    border-width: 2px;
  }
  
  .text-gray-500 {
    color: rgb(0, 0, 0);
  }
}

/* 打印样式 */
@media print {
  .backdrop-blur-xl,
  .shadow-xl,
  .shadow-lg {
    backdrop-filter: none;
    box-shadow: none;
  }

  .bg-gradient-to-br {
    background: white;
  }
}

/* 拖拽时禁用模糊效果以提升性能 */
.disable-blur .backdrop-blur-xl {
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

.disable-blur .shadow-xl,
.disable-blur .shadow-lg {
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1) !important;
}
</style>