use image::{ImageBuffer, Rgb, RgbImage};
use noise::{NoiseFn, Perlin};
use wasm_bindgen::prelude::*;
use std::io::Cursor;
use base64::{Engine as _, engine::general_purpose};

#[wasm_bindgen]
pub fn apply_perlin_noise(
    base64_img: String,
    intensity: f32,
    scale: f32,
    octaves: u32,
) -> Result<String, JsValue> {
    // 解码 Base64
    let img_data = general_purpose::STANDARD
        .decode(&base64_img)
        .map_err(|e| JsValue::from_str(&format!("Failed to decode base64: {:?}", e)))?;

    // 加载图像
    let img = image::load_from_memory(&img_data)
        .map_err(|e| JsValue::from_str(&format!("Failed to load image: {:?}", e)))?
        .to_rgb8();

    let (width, height) = img.dimensions();
    let mut result: RgbImage = ImageBuffer::new(width, height);

    // 创建 Perlin 噪声生成器
    let perlin = Perlin::new(rand::random());

    // 应用噪声
    for y in 0..height {
        for x in 0..width {
            let pixel = img.get_pixel(x, y);

            // 计算多 octave 噪声
            let mut noise_val = 0.0;
            let mut amplitude = 1.0;
            let mut frequency = 1.0;
            let mut max_val = 0.0;

            for _ in 0..octaves {
                let nx = x as f64 / scale as f64 * frequency;
                let ny = y as f64 / scale as f64 * frequency;
                noise_val += perlin.get([nx, ny]) * amplitude;
                max_val += amplitude;
                amplitude *= 0.5;
                frequency *= 2.0;
            }

            noise_val /= max_val;
            let noise = (noise_val * intensity as f64 * 255.0) as i32;

            // 应用噪声到像素
            let r = (pixel[0] as i32 + noise).clamp(0, 255) as u8;
            let g = (pixel[1] as i32 + noise).clamp(0, 255) as u8;
            let b = (pixel[2] as i32 + noise).clamp(0, 255) as u8;

            result.put_pixel(x, y, Rgb([r, g, b]));
        }
    }

    // 编码回 Base64
    encode_to_base64(&result)
}

#[wasm_bindgen]
pub fn apply_vignette(
    base64_img: String,
    intensity: f32,
    spread: f32,
) -> Result<String, JsValue> {
    // 解码 Base64
    let img_data = general_purpose::STANDARD
        .decode(&base64_img)
        .map_err(|e| JsValue::from_str(&format!("Failed to decode base64: {:?}", e)))?;

    // 加载图像
    let img = image::load_from_memory(&img_data)
        .map_err(|e| JsValue::from_str(&format!("Failed to load image: {:?}", e)))?
        .to_rgb8();

    let (width, height) = img.dimensions();
    let mut result: RgbImage = ImageBuffer::new(width, height);

    let cx = width as f32 / 2.0;
    let cy = height as f32 / 2.0;
    let max_dist = (cx * cx + cy * cy).sqrt();

    for y in 0..height {
        for x in 0..width {
            let pixel = img.get_pixel(x, y);

            let dx = x as f32 - cx;
            let dy = y as f32 - cy;
            let dist = (dx * dx + dy * dy).sqrt();
            let norm_dist = dist / max_dist;

            let adjusted_dist = ((norm_dist - spread) / (1.0 - spread)).clamp(0.0, 1.0);
            let vignette_factor = 1.0 - (adjusted_dist * intensity);

            let r = (pixel[0] as f32 * vignette_factor) as u8;
            let g = (pixel[1] as f32 * vignette_factor) as u8;
            let b = (pixel[2] as f32 * vignette_factor) as u8;

            result.put_pixel(x, y, Rgb([r, g, b]));
        }
    }

    encode_to_base64(&result)
}

#[wasm_bindgen]
pub fn apply_frosted_glass(
    base64_img: String,
    intensity: f32,
) -> Result<String, JsValue> {
    // 先应用轻微模糊，然后添加噪声
    // 这里简化实现，实际可以使用高斯模糊
    apply_perlin_noise(base64_img, intensity * 0.6, 30.0, 2)
}

#[wasm_bindgen]
pub fn apply_film_grain(
    base64_img: String,
    intensity: f32,
) -> Result<String, JsValue> {
    // 组合 Perlin 噪声和随机噪声
    apply_perlin_noise(base64_img, intensity * 0.6, 40.0, 3)
}

fn encode_to_base64(img: &RgbImage) -> Result<String, JsValue> {
    let mut buffer = Cursor::new(Vec::new());
    img.write_to(&mut buffer, image::ImageOutputFormat::Png)
        .map_err(|e| JsValue::from_str(&format!("Failed to encode PNG: {:?}", e)))?;

    let base64_str = general_purpose::STANDARD.encode(buffer.into_inner());
    Ok(base64_str)
}

// 添加随机数生成支持
mod rand {
    use std::cell::RefCell;

    thread_local! {
        static RNG_STATE: RefCell<u64> = RefCell::new(1);
    }

    pub fn random() -> u32 {
        RNG_STATE.with(|state| {
            let mut s = state.borrow_mut();
            *s = s.wrapping_mul(6364136223846793005).wrapping_add(1);
            (*s >> 32) as u32
        })
    }
}
