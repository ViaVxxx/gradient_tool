use serde::{Deserialize, Serialize};
use tauri_plugin_dialog::DialogExt;

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ColorStop {
    position: f32,
    color: ColorData,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ColorData {
    r: u8,
    g: u8,
    b: u8,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Preset {
    name: String,
    category: String,
    gradient_type: String,
    angle: f32,
    stops: Vec<ColorStop>,
}

#[tauri::command]
fn get_presets(category: Option<String>) -> Result<Vec<Preset>, String> {
    // 从嵌入的 JSON 加载预设
    let presets_json = include_str!("../assets/presets.json");
    let all_presets: Vec<Preset> = serde_json::from_str(presets_json)
        .map_err(|e| format!("Failed to parse presets: {}", e))?;

    Ok(match category {
        Some(cat) => all_presets
            .into_iter()
            .filter(|p| p.category == cat)
            .collect(),
        None => all_presets,
    })
}

#[tauri::command]
async fn save_image(
    app: tauri::AppHandle,
    image_data_base64: String,
    _format: String,
) -> Result<String, String> {
    use base64::{Engine as _, engine::general_purpose};
    use std::fs;
    use std::path::PathBuf;

    // 打开保存对话框
    let file_path = app.dialog()
        .file()
        .set_title("保存渐变图像")
        .add_filter("PNG", &["png"])
        .add_filter("JPEG", &["jpg", "jpeg"])
        .blocking_save_file()
        .ok_or("用户取消保存")?;

    // 获取路径
    let path = PathBuf::from(file_path.to_string());

    // 解码 Base64
    let img_data = general_purpose::STANDARD
        .decode(&image_data_base64)
        .map_err(|e| format!("Base64 解码失败: {}", e))?;

    // 写入文件
    fs::write(&path, img_data).map_err(|e| format!("文件写入失败: {}", e))?;

    Ok(path.to_string_lossy().to_string())
}

#[tauri::command]
fn get_app_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_dialog::init())
        .setup(|app| {
            if cfg!(debug_assertions) {
                app.handle().plugin(
                    tauri_plugin_log::Builder::default()
                        .level(log::LevelFilter::Info)
                        .build(),
                )?;
            }
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![
            get_presets,
            save_image,
            get_app_version
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
