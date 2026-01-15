import { generateGradient, applyEffect, initWasm } from './wasm';
import { getPresets, exportImage, getAppVersion } from './tauri';

// 统一 API 接口，兼容原 PyWebView API
export const api = {
  generate_gradient: async (type, stops, angle = 0, cx = 0.5, cy = 0.5) => {
    return await generateGradient(type, stops, angle, cx, cy);
  },

  apply_effect: async (type, intensity) => {
    // 需要当前图像，从全局状态获取
    const currentImage = window.__currentGradientImage__;
    if (!currentImage) {
      return { success: false, error: '没有可用的图像' };
    }
    return await applyEffect(type, intensity, currentImage);
  },

  get_presets: async (category = null) => {
    return await getPresets(category);
  },

  export_image: async (format = 'png', quality = 95) => {
    const currentImage = window.__currentGradientImage__;
    if (!currentImage) {
      return { success: false, error: '没有可用的图像' };
    }
    return await exportImage(currentImage, format);
  },

  get_app_version: async () => {
    return await getAppVersion();
  },
};

// 预加载 WASM
export async function preloadWasm() {
  try {
    await initWasm();
    console.log('✓ WASM 模块已加载');
  } catch (error) {
    console.error('✗ WASM 加载失败:', error);
  }
}

// 兼容旧代码：模拟 PyWebView API
if (typeof window !== 'undefined') {
  window.pywebview = { api };
}

export default api;
