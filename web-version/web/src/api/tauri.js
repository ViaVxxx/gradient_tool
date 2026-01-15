import { invoke } from '@tauri-apps/api/core';

export async function getPresets(category = null) {
  try {
    return await invoke('get_presets', { category });
  } catch (error) {
    console.error('获取预设失败:', error);
    return [];
  }
}

export async function exportImage(imageDataBase64, format = 'png') {
  try {
    // 从 data URL 提取 base64
    const base64 = imageDataBase64.split(',')[1];
    const filepath = await invoke('save_image', {
      imageDataBase64: base64,
      format,
    });
    return { success: true, filepath };
  } catch (error) {
    console.error('导出图像失败:', error);
    return { success: false, error: error.toString() };
  }
}

export async function getAppVersion() {
  try {
    return await invoke('get_app_version');
  } catch (error) {
    console.error('获取版本失败:', error);
    return '未知版本';
  }
}
