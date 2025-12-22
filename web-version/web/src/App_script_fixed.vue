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
const isGenerating = ref(false)
const presets = ref([])
const apiReady = ref(false)

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

// 等待 PyWebView API 准备好
async function waitForAPI() {
  return new Promise((resolve) => {
    const checkAPI = () => {
      if (window.pywebview && window.pywebview.api) {
        apiReady.value = true
        resolve(true)
      } else {
        setTimeout(checkAPI, 100)
      }
    }
    checkAPI()
  })
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

// 生成渐变
async function generateGradient() {
  if (!apiReady.value) {
    alert('正在初始化，请稍候...')
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
async function applyEffect(effectType) {
  if (!apiReady.value) {
    alert('正在初始化，请稍候...')
    await waitForAPI()
  }

  if (!generatedImage.value) {
    await generateGradient()
  }

  isGenerating.value = true
  try {
    const result = await window.pywebview.api.apply_effect(effectType, 0.2)

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
async function randomGradient() {
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
  await generateGradient()
}

// 导出图像
async function exportImage() {
  if (!apiReady.value) {
    alert('正在初始化，请稍候...')
    return
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
async function loadPreset(preset) {
  gradientType.value = preset.gradient_type
  angle.value = preset.angle || 90

  colorStops.value = preset.stops.map(stop => ({
    position: stop.position,
    color: stop.color,
    hex: rgbToHex(stop.color.r, stop.color.g, stop.color.b)
  }))

  await generateGradient()
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
    // 如果是开发模式（直接在浏览器打开），使用模拟数据
    if (!window.pywebview) {
      console.log('开发模式：使用模拟数据')
      presets.value = [
        {
          name: '紫色梦幻',
          gradient_type: 'linear',
          angle: 135,
          stops: [
            { position: 0, color: { r: 102, g: 126, b: 234 } },
            { position: 1, color: { r: 118, g: 75, b: 162 } }
          ]
        }
      ]
    }
  }
}

// 组件挂载
onMounted(async () => {
  console.log('组件已挂载，等待 API 准备...')
  await waitForAPI()
  console.log('API 已准备好')

  await loadPresets()
  await generateGradient()
})

// 监听变化自动更新预览
watch([gradientType, angle, colorStops], () => {
  // 实时预览会自动更新，无需手动调用
}, { deep: true })
</script>
