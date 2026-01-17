import { reactive, computed, toRefs } from 'vue'
import { api, preloadWasm } from '@/api'

// 全局状态
const state = reactive({
  // 渐变配置
  gradientType: 'linear',
  angle: 90,
  colorStops: [
    { position: 0, color: { r: 42, g: 123, b: 155 }, hex: '#2A7B9B', alpha: 100 },
    { position: 0.4, color: { r: 87, g: 199, b: 133 }, hex: '#57C785', alpha: 100 },
    { position: 0.62, color: { r: 143, g: 207, b: 114 }, hex: '#8FCF72', alpha: 100 },
    { position: 1, color: { r: 237, g: 221, b: 83 }, hex: '#EDDD53', alpha: 100 }
  ],
  selectedColorStopIndex: 0,

  // 图像状态
  generatedImage: null,
  originalImage: null,
  isGenerating: false,
  loadingText: '生成中...',
  loadingProgress: 0,

  // 效果状态
  effectsEnabled: {
    perlin: false,
    frosted: false,
    film: false,
    vignette: false
  },
  effectIntensities: {
    perlin: 0.3,
    frosted: 0.2,
    film: 0.25,
    vignette: 0.5
  },
  lastAppliedEffect: null,

  // UI 状态
  previewMode: 'css',
  isFullscreen: false,
  isPureMode: false,
  isDragging: false,

  // 预设
  presets: [],
  selectedPresetCategory: '',

  // API 状态
  apiReady: false
})

// 颜色转换工具
export function hexToRgb(hex) {
  const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex)
  return result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null
}

export function rgbToHex(r, g, b) {
  return '#' + [r, g, b].map(x => {
    const hex = x.toString(16)
    return hex.length === 1 ? '0' + hex : hex
  }).join('')
}

// 颜色插值工具
export function interpolateColorAtPosition(colorStops, position) {
  const stops = [...colorStops].sort((a, b) => a.position - b.position)

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

// 计算属性
const previewStyle = computed(() => {
  const stops = state.colorStops.map(stop => {
    const { r, g, b } = stop.color
    return `rgb(${r},${g},${b}) ${stop.position * 100}%`
  }).join(', ')

  if (state.gradientType === 'linear') {
    return {
      background: `linear-gradient(${state.angle}deg, ${stops})`
    }
  } else {
    return {
      background: `radial-gradient(circle, ${stops})`
    }
  }
})

const filteredPresets = computed(() => {
  if (!state.selectedPresetCategory) return state.presets
  return state.presets.filter(preset => preset.category === state.selectedPresetCategory)
})

// API 方法
async function waitForAPI() {
  try {
    await preloadWasm()
    state.apiReady = true
    console.log('✓ WASM + Tauri API 已准备好')
    return true
  } catch (error) {
    console.error('✗ API 初始化失败:', error)
    return false
  }
}

async function generateGradient() {
  if (!state.apiReady) {
    await waitForAPI()
  }

  state.isGenerating = true
  state.loadingText = '正在生成渐变...'
  state.loadingProgress = 0

  const progressInterval = setInterval(() => {
    if (state.loadingProgress < 90) {
      state.loadingProgress += Math.random() * 20
    }
  }, 200)

  try {
    const result = await api.generate_gradient(
      state.gradientType,
      state.colorStops,
      state.angle
    )

    clearInterval(progressInterval)
    state.loadingProgress = 100

    if (result.success) {
      state.generatedImage = result.image
      state.originalImage = result.image
      window.__currentGradientImage__ = result.image
      state.lastAppliedEffect = null
      state.previewMode = 'image'
    } else {
      alert('生成失败: ' + result.error)
    }
  } catch (error) {
    clearInterval(progressInterval)
    console.error('生成错误:', error)
    alert('生成失败: ' + error.message)
  } finally {
    state.isGenerating = false
    state.loadingProgress = 0
  }
}

async function applyEffect(effectType, intensity = null) {
  if (!state.apiReady) {
    await waitForAPI()
  }

  if (!state.originalImage) {
    await generateGradient()
  }

  state.lastAppliedEffect = effectType
  state.isGenerating = true
  state.loadingText = `正在应用效果...`

  try {
    const effectIntensity = intensity !== null ? intensity : state.effectIntensities[effectType]

    // 修复：基于原始图像重新计算整个效果链
    await applyEffectPipeline()
  } catch (error) {
    console.error('效果错误:', error)
    alert('应用效果失败: ' + error.message)
  } finally {
    state.isGenerating = false
  }
}

// 新增：效果管线 - 基于原始图像按顺序应用所有启用的效果
async function applyEffectPipeline() {
  if (!state.originalImage) {
    return
  }

  let currentImage = state.originalImage

  // 按顺序应用所有启用的效果
  const effectOrder = ['perlin', 'frosted', 'film', 'vignette']

  for (const effectType of effectOrder) {
    if (state.effectsEnabled[effectType]) {
      const intensity = state.effectIntensities[effectType]
      const result = await api.apply_effect(effectType, intensity, currentImage)

      if (result.success) {
        currentImage = result.image
      } else {
        console.error(`应用 ${effectType} 效果失败:`, result.error)
        break
      }
    }
  }

  state.generatedImage = currentImage
  window.__currentGradientImage__ = currentImage
  state.previewMode = 'image'
}

async function exportImage() {
  if (!state.apiReady) {
    await waitForAPI()
  }

  if (!state.generatedImage) {
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

function copyCSS() {
  const stops = state.colorStops.map(stop => {
    const { r, g, b } = stop.color
    return `rgb(${r},${g},${b}) ${stop.position * 100}%`
  }).join(', ')

  let cssText = ''
  if (state.gradientType === 'linear') {
    cssText = `background: linear-gradient(${state.angle}deg, ${stops});`
  } else {
    cssText = `background: radial-gradient(circle, ${stops});`
  }

  navigator.clipboard.writeText(cssText).then(() => {
    alert('CSS 代码已复制到剪贴板')
  }).catch(() => {
    alert('复制失败，请手动复制')
  })
}

function randomGradient() {
  const count = Math.floor(Math.random() * 3) + 2
  state.colorStops = []

  for (let i = 0; i < count; i++) {
    const r = Math.floor(Math.random() * 256)
    const g = Math.floor(Math.random() * 256)
    const b = Math.floor(Math.random() * 256)

    state.colorStops.push({
      position: i / (count - 1),
      color: { r, g, b },
      hex: rgbToHex(r, g, b),
      alpha: 100
    })
  }

  state.selectedColorStopIndex = null
  state.angle = Math.floor(Math.random() * 360)
  generateGradient()
}

async function loadPresets() {
  if (!state.apiReady) {
    await waitForAPI()
  }

  try {
    state.presets = await api.get_presets()
  } catch (error) {
    console.error('加载预设失败:', error)
  }
}

function loadPreset(preset) {
  state.gradientType = preset.gradient_type
  state.angle = preset.angle || 90

  state.colorStops = preset.stops.map(stop => ({
    position: stop.position,
    color: stop.color,
    hex: rgbToHex(stop.color.r, stop.color.g, stop.color.b),
    alpha: 100
  }))

  state.selectedColorStopIndex = null
  generateGradient()
}

// 恢复到原始图像（增强方案 A）
function resetToOriginalImage() {
  if (!state.originalImage) return
  state.generatedImage = state.originalImage
  window.__currentGradientImage__ = state.originalImage
  state.lastAppliedEffect = null
  state.previewMode = 'image'
}

// 切换全屏模式（改为 Zen Mode - 窗口内沉浸模式）
function toggleFullscreen() {
  // 仅切换 isPureMode 状态，不调用系统全屏
  // Sidebar 和 Toolbar 通过 CSS 响应 isPureMode 变化
  state.isPureMode = !state.isPureMode
}

// 导出 composable
export function useGradient() {
  return {
    // 状态
    ...toRefs(state),

    // 计算属性
    previewStyle,
    filteredPresets,

    // 方法
    waitForAPI,
    generateGradient,
    applyEffect,
    exportImage,
    copyCSS,
    randomGradient,
    loadPresets,
    loadPreset,
    resetToOriginalImage,
    toggleFullscreen,

    // 工具函数
    hexToRgb,
    rgbToHex,
    interpolateColorAtPosition
  }
}
