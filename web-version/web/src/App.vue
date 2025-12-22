<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 现代化头部 -->
    <header class="bg-white border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-3">
            <div class="w-9 h-9 rounded-lg bg-indigo-600 flex items-center justify-center">
              <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
              </svg>
            </div>
            <div>
              <h1 class="text-xl font-bold text-gray-900">
                Gradient Tool
              </h1>
              <p class="text-xs text-gray-500">专业渐变图像生成器</p>
            </div>
          </div>

          <div class="flex items-center space-x-2">
            <button @click="randomGradient"
                    class="px-4 py-2 rounded-lg bg-gray-100 text-gray-700 hover:bg-gray-200 text-sm font-medium transition-colors">
              <span class="flex items-center space-x-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                </svg>
                <span>随机</span>
              </span>
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- 主内容区 -->
    <main class="max-w-7xl mx-auto px-6 py-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">

        <!-- 左栏：渐变设计控制 -->
        <div class="lg:col-span-3 space-y-6">

          <!-- 渐变类型卡片 -->
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <h3 class="text-sm font-semibold text-gray-700 mb-3">渐变类型</h3>
            <div class="grid grid-cols-2 gap-2">
              <button
                v-for="type in gradientTypes"
                :key="type.value"
                @click="gradientType = type.value"
                :class="[
                  'px-3 py-2 rounded-lg text-sm font-medium transition-all duration-200',
                  gradientType === type.value
                    ? 'bg-indigo-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                ]">
                {{ type.label }}
              </button>
            </div>
          </div>

          <!-- 色标编辑器 -->
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <div class="flex items-center justify-between mb-3">
              <h3 class="text-sm font-semibold text-gray-700">色标</h3>
              <button @click="addColorStop"
                      class="px-2 py-1 rounded text-xs bg-indigo-50 text-indigo-600 hover:bg-indigo-100 transition-colors">
                + 添加
              </button>
            </div>

            <!-- 水平渐变条预览 -->
            <div class="relative h-8 rounded-lg mb-3 border border-gray-200 overflow-hidden"
                 :style="previewStyle">
            </div>

            <!-- 紧凑色标列表 -->
            <div class="space-y-2">
              <div v-for="(stop, index) in colorStops" :key="index"
                   class="flex items-center gap-2 text-sm">
                <input
                  type="color"
                  v-model="stop.hex"
                  @change="updateColorFromHex(index)"
                  class="w-8 h-8 rounded cursor-pointer border border-gray-300">

                <input
                  type="number"
                  v-model.number="stop.position"
                  min="0"
                  max="1"
                  step="0.01"
                  class="w-16 px-2 py-1 border border-gray-300 rounded text-xs font-mono text-center">

                <span class="text-xs text-gray-500 font-mono">{{ Math.round(stop.position * 100) }}%</span>

                <div class="flex-1"></div>

                <button v-if="colorStops.length > 2"
                        @click="removeColorStop(index)"
                        class="p-1 text-gray-400 hover:text-red-500 transition-colors">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>

          <!-- 角度控制（仅线性渐变） -->
          <div v-if="gradientType === 'linear'"
               class="bg-white rounded-lg border border-gray-200 p-5">
            <h3 class="text-sm font-semibold text-gray-700 mb-3">角度</h3>
            <div class="flex items-center gap-4">
              <!-- 圆盘选择器 -->
              <div class="relative w-24 h-24">
                <svg class="w-full h-full" viewBox="0 0 100 100">
                  <!-- 外圈 -->
                  <circle cx="50" cy="50" r="45" fill="none" stroke="#E5E7EB" stroke-width="2"/>
                  <!-- 刻度线 -->
                  <line x1="50" y1="5" x2="50" y2="12" stroke="#9CA3AF" stroke-width="1.5"/>
                  <line x1="95" y1="50" x2="88" y2="50" stroke="#9CA3AF" stroke-width="1.5"/>
                  <line x1="50" y1="95" x2="50" y2="88" stroke="#9CA3AF" stroke-width="1.5"/>
                  <line x1="5" y1="50" x2="12" y2="50" stroke="#9CA3AF" stroke-width="1.5"/>
                  <!-- 指针 -->
                  <line
                    :x1="50"
                    :y1="50"
                    :x2="50 + 35 * Math.cos((angle - 90) * Math.PI / 180)"
                    :y2="50 + 35 * Math.sin((angle - 90) * Math.PI / 180)"
                    stroke="#6366F1"
                    stroke-width="2.5"
                    stroke-linecap="round"/>
                  <!-- 中心点 -->
                  <circle cx="50" cy="50" r="4" fill="#6366F1"/>
                </svg>
                <!-- 交互层 -->
                <div
                  class="absolute inset-0 cursor-pointer"
                  @mousedown="startAngleDrag"
                  @touchstart="startAngleDrag">
                </div>
              </div>

              <!-- 数字输入 -->
              <div class="flex-1">
                <input
                  type="number"
                  v-model.number="angle"
                  min="0"
                  max="360"
                  step="1"
                  class="w-full px-3 py-2 border border-gray-300 rounded text-center text-2xl font-mono font-bold text-indigo-600">
                <div class="text-xs text-gray-500 text-center mt-1">度 (°)</div>
              </div>
            </div>
          </div>
        </div>

        <!-- 中栏：预览区域 -->
        <div class="lg:col-span-6">
          <div class="bg-white rounded-lg border border-gray-200 p-5 h-full">
            <div class="flex items-center justify-between mb-4">
              <h3 class="text-sm font-semibold text-gray-700">预览</h3>
              <div class="flex items-center gap-3">
                <div class="flex items-center gap-1.5 text-xs text-gray-500">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span class="font-mono">800 × 600</span>
                </div>
                <button @click="exportImage"
                        class="px-3 py-1.5 rounded-lg text-xs font-medium bg-gray-100 text-gray-700 hover:bg-gray-200 transition-colors">
                  导出 PNG
                </button>
              </div>
            </div>

            <!-- 渐变预览画布 -->
            <div class="relative rounded-lg overflow-hidden border border-gray-200" style="aspect-ratio: 4/3;">
              <div
                v-if="!generatedImage"
                class="absolute inset-0 flex items-center justify-center"
                :style="previewStyle">
                <div class="text-center">
                  <svg class="w-12 h-12 mx-auto text-white/40 mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                  </svg>
                  <p class="text-xs text-white/60 font-medium">实时预览</p>
                </div>
              </div>

              <img
                v-else
                :src="generatedImage"
                alt="Generated gradient"
                class="absolute inset-0 w-full h-full object-cover">

              <!-- 生成中加载状态 -->
              <div v-if="isGenerating"
                   class="absolute inset-0 bg-white/80 backdrop-blur-sm flex items-center justify-center">
                <div class="text-center">
                  <div class="w-10 h-10 border-3 border-gray-200 border-t-indigo-600 rounded-full animate-spin mx-auto mb-2"></div>
                  <p class="text-sm text-gray-600 font-medium">生成中...</p>
                </div>
              </div>
            </div>

            <!-- 操作按钮 -->
            <div class="mt-4">
              <button @click="generateGradient"
                      :disabled="isGenerating"
                      class="w-full px-6 py-2.5 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
                <span class="flex items-center justify-center gap-2">
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  <span>生成渐变</span>
                </span>
              </button>
            </div>
          </div>
        </div>

        <!-- 右栏：效果和预设 -->
        <div class="lg:col-span-3 space-y-6">

          <!-- 纹理效果 -->
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <h3 class="text-sm font-semibold text-gray-700 mb-3">纹理效果</h3>
            <div class="space-y-3">
              <div
                v-for="effect in effects"
                :key="effect.value"
                class="border border-gray-200 rounded-lg overflow-hidden"
                :class="effectsEnabled[effect.value] ? 'border-indigo-200 bg-indigo-50/30' : 'bg-gray-50/50'">

                <!-- 效果头部（开关） -->
                <div class="flex items-center justify-between p-3">
                  <label class="flex items-center gap-2 cursor-pointer flex-1">
                    <input
                      type="checkbox"
                      v-model="effectsEnabled[effect.value]"
                      @change="toggleEffect(effect.value)"
                      class="w-4 h-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                    <span class="text-sm font-medium" :class="effectsEnabled[effect.value] ? 'text-gray-900' : 'text-gray-500'">
                      {{ effect.label }}
                    </span>
                  </label>
                </div>

                <!-- 强度滑块（仅开启时显示） -->
                <div v-if="effectsEnabled[effect.value]" class="px-3 pb-3 space-y-1">
                  <div class="flex items-center justify-between">
                    <span class="text-xs text-gray-500">强度</span>
                    <span class="text-xs font-mono font-semibold text-indigo-600">{{ Math.round(effectIntensities[effect.value] * 100) }}%</span>
                  </div>
                  <input
                    type="range"
                    v-model.number="effectIntensities[effect.value]"
                    min="0.1"
                    max="1"
                    step="0.05"
                    class="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer slider">
                </div>
              </div>
            </div>
          </div>

          <!-- 预设库 -->
          <div class="bg-white rounded-lg border border-gray-200 p-5">
            <h3 class="text-sm font-semibold text-gray-700 mb-3">预设渐变</h3>
            <div class="grid grid-cols-2 gap-2 max-h-96 overflow-y-auto">
              <button
                v-for="preset in presets"
                :key="preset.name"
                @click="loadPreset(preset)"
                class="group relative h-16 rounded-lg overflow-hidden border border-gray-200 hover:border-indigo-300 transition-all duration-200">
                <div
                  class="absolute inset-0"
                  :style="getPresetStyle(preset)">
                </div>
                <div class="absolute inset-0 bg-gradient-to-t from-black/70 to-transparent opacity-0 group-hover:opacity-100 transition-opacity flex items-end p-2">
                  <span class="text-xs text-white font-medium truncate">{{ preset.name }}</span>
                </div>
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted } from 'vue'

// 响应式数据
const gradientType = ref('linear')
const angle = ref(90)
const colorStops = ref([
  { position: 0, color: { r: 102, g: 126, b: 234 }, hex: '#667eea' },
  { position: 1, color: { r: 118, g: 75, b: 162 }, hex: '#764ba2' }
])
const generatedImage = ref(null)
const originalImage = ref(null) // 保存原始渐变图像（未应用效果）
const isGenerating = ref(false)
const presets = ref([])
const apiReady = ref(false)
const lastAppliedEffect = ref(null) // 记录最后应用的效果类型
const effectsEnabled = ref({
  perlin: false,
  frosted: false,
  film: false,
  vignette: false
})

// 等待 PyWebView API 准备好
async function waitForAPI() {
  return new Promise((resolve) => {
    const checkAPI = () => {
      if (window.pywebview && window.pywebview.api) {
        apiReady.value = true
        console.log('✓ PyWebView API 已准备好')
        resolve(true)
      } else {
        setTimeout(checkAPI, 100)
      }
    }
    checkAPI()
  })
}

// 渐变类型选项
const gradientTypes = [
  { label: '线性渐变', value: 'linear' },
  { label: '径向渐变', value: 'radial' }
]

// 纹理效果选项
const effects = [
  { label: '✨ Perlin 噪点', value: 'perlin' },
  { label: '🌫️ 磨砂玻璃', value: 'frosted' },
  { label: '🎞️ 胶片颗粒', value: 'film' },
  { label: '🎭 晕影效果', value: 'vignette' }
]

// 效果强度
const effectIntensities = ref({
  perlin: 0.3,
  frosted: 0.2,
  film: 0.25,
  vignette: 0.5
})

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

// 色标管理
function addColorStop() {
  if (colorStops.value.length >= 20) return
  colorStops.value.push({
    position: 0.5,
    color: { r: 128, g: 128, b: 128 },
    hex: '#808080'
  })
}

function removeColorStop(index) {
  if (colorStops.value.length <= 2) return
  colorStops.value.splice(index, 1)
}

// 圆盘角度拖动
function startAngleDrag(e) {
  e.preventDefault()

  const updateAngle = (clientX, clientY) => {
    const target = e.currentTarget
    const rect = target.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2

    const deltaX = clientX - centerX
    const deltaY = clientY - centerY

    let newAngle = Math.atan2(deltaY, deltaX) * 180 / Math.PI + 90
    if (newAngle < 0) newAngle += 360

    angle.value = Math.round(newAngle)
  }

  const handleMove = (e) => {
    const clientX = e.touches ? e.touches[0].clientX : e.clientX
    const clientY = e.touches ? e.touches[0].clientY : e.clientY
    updateAngle(clientX, clientY)
  }

  const handleEnd = () => {
    document.removeEventListener('mousemove', handleMove)
    document.removeEventListener('mouseup', handleEnd)
    document.removeEventListener('touchmove', handleMove)
    document.removeEventListener('touchend', handleEnd)
  }

  document.addEventListener('mousemove', handleMove)
  document.addEventListener('mouseup', handleEnd)
  document.addEventListener('touchmove', handleMove)
  document.addEventListener('touchend', handleEnd)

  // 初始位置
  const clientX = e.touches ? e.touches[0].clientX : e.clientX
  const clientY = e.touches ? e.touches[0].clientY : e.clientY
  updateAngle(clientX, clientY)
}

// 切换效果开关
function toggleEffect(effectType) {
  // v-model 已经自动切换了值，这里只需要根据新值执行操作
  if (effectsEnabled.value[effectType]) {
    // 开启效果时，确保强度不会太低（至少10%）
    if (effectIntensities.value[effectType] < 0.1) {
      effectIntensities.value[effectType] = 0.3 // 设置为推荐值
    }
    // 应用效果
    applyEffect(effectType)
  } else {
    // 关闭效果，恢复原图
    if (originalImage.value) {
      generatedImage.value = originalImage.value
      lastAppliedEffect.value = null
    }
  }
}

// 生成渐变
async function generateGradient() {
  if (!apiReady.value) {
    console.log('等待 API 准备...')
    await waitForAPI()
  }

  isGenerating.value = true
  try {
    const result = await window.pywebview.api.generate_gradient(
      gradientType.value,
      colorStops.value,
      angle.value
    )

    if (result.success) {
      generatedImage.value = result.image
      originalImage.value = result.image // 保存原始图像
      lastAppliedEffect.value = null // 清除效果记录
    } else {
      alert('生成失败: ' + result.error)
    }
  } catch (error) {
    console.error('生成错误:', error)
    alert('生成失败: ' + error.message)
  } finally {
    isGenerating.value = false
  }
}

// 应用效果
async function applyEffect(effectType, intensity = null) {
  if (!apiReady.value) {
    console.log('等待 API 准备...')
    await waitForAPI()
  }

  if (!originalImage.value) {
    await generateGradient()
  }

  // 记录最后应用的效果
  lastAppliedEffect.value = effectType

  isGenerating.value = true
  try {
    // 使用对应效果的强度值（如果没有传入则使用当前设置）
    const effectIntensity = intensity !== null ? intensity : effectIntensities.value[effectType]
    const result = await window.pywebview.api.apply_effect(effectType, effectIntensity)

    if (result.success) {
      generatedImage.value = result.image
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
  // 随机2-4个色标
  const count = Math.floor(Math.random() * 3) + 2
  colorStops.value = []

  for (let i = 0; i < count; i++) {
    const r = Math.floor(Math.random() * 256)
    const g = Math.floor(Math.random() * 256)
    const b = Math.floor(Math.random() * 256)

    colorStops.value.push({
      position: i / (count - 1),
      color: { r, g, b },
      hex: rgbToHex(r, g, b)
    })
  }

  angle.value = Math.floor(Math.random() * 360)
  generateGradient()
}

// 导出图像
async function exportImage() {
  if (!apiReady.value) {
    alert('正在初始化，请稍候...')
    await waitForAPI()
  }

  if (!generatedImage.value) {
    alert('请先生成渐变')
    return
  }

  try {
    const result = await window.pywebview.api.export_image('png', 95)

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

// 加载预设
function loadPreset(preset) {
  gradientType.value = preset.gradient_type
  angle.value = preset.angle || 90

  colorStops.value = preset.stops.map(stop => ({
    position: stop.position,
    color: stop.color,
    hex: rgbToHex(stop.color.r, stop.color.g, stop.color.b)
  }))

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

// 加载预设列表
async function loadPresets() {
  if (!apiReady.value) {
    await waitForAPI()
  }

  try {
    presets.value = await window.pywebview.api.get_presets()
  } catch (error) {
    console.error('加载预设失败:', error)
  }
}

// 组件挂载
onMounted(async () => {
  console.log('组件已挂载，等待 API 准备...')
  await waitForAPI()
  console.log('开始加载预设和生成渐变...')

  await loadPresets()
  await generateGradient()
})

// 监听变化自动更新预览
watch([gradientType, angle, colorStops], () => {
  // 实时预览会自动更新，无需手动调用
}, { deep: true })

// 监听效果强度变化，自动重新应用效果
let debounceTimer = null
watch(effectIntensities, () => {
  // 只有在有效果被开启后才自动更新
  if (!lastAppliedEffect.value || !originalImage.value || !effectsEnabled.value[lastAppliedEffect.value]) return

  // 清除之前的定时器
  if (debounceTimer) {
    clearTimeout(debounceTimer)
  }

  // 防抖：500ms 后自动应用效果
  debounceTimer = setTimeout(() => {
    if (!isGenerating.value) {
      applyEffect(lastAppliedEffect.value)
    }
  }, 500)
}, { deep: true })
</script>

<style>
/* 自定义滑块样式 */
.slider::-webkit-slider-thumb {
  appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #6366F1;
  cursor: pointer;
  box-shadow: 0 1px 3px rgba(99, 102, 241, 0.3);
  transition: all 0.2s;
}

.slider::-webkit-slider-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 6px rgba(99, 102, 241, 0.4);
}

.slider::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: #6366F1;
  cursor: pointer;
  border: none;
  box-shadow: 0 1px 3px rgba(99, 102, 241, 0.3);
  transition: all 0.2s;
}

.slider::-moz-range-thumb:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 6px rgba(99, 102, 241, 0.4);
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 6px;
}

::-webkit-scrollbar-track {
  background: #F3F4F6;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb {
  background: #D1D5DB;
  border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
  background: #9CA3AF;
}
</style>
