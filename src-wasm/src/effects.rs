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

            // 使用 Smoothstep 曲线替代线性插值
            let smooth_factor = adjusted_dist * adjusted_dist * (3.0 - 2.0 * adjusted_dist);
            let vignette_factor = 1.0 - (smooth_factor * intensity);

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
    // 解码 Base64
    let img_data = general_purpose::STANDARD
        .decode(&base64_img)
        .map_err(|e| JsValue::from_str(&format!("Failed to decode base64: {:?}", e)))?;

    // 加载图像
    let img = image::load_from_memory(&img_data)
        .map_err(|e| JsValue::from_str(&format!("Failed to load image: {:?}", e)))?
        .to_rgb8();

    let (width, height) = img.dimensions();

    // 1. 应用高斯模糊（磨砂玻璃的核心）
    let blur_radius = (intensity * 15.0).max(0.5);
    let mut blurred = apply_box_blur(&img, blur_radius as u32);

    // 2. 添加微弱白噪声（表面质感）
    let noise_intensity = intensity * 0.08;
    add_white_noise(&mut blurred, noise_intensity);

    // 3. 轻微提亮（模拟光散射）
    let brightness_boost = 1.0 + (intensity * 0.05);
    for pixel in blurred.pixels_mut() {
        pixel[0] = ((pixel[0] as f32 * brightness_boost).min(255.0)) as u8;
        pixel[1] = ((pixel[1] as f32 * brightness_boost).min(255.0)) as u8;
        pixel[2] = ((pixel[2] as f32 * brightness_boost).min(255.0)) as u8;
    }

    encode_to_base64(&blurred)
}

#[wasm_bindgen]
pub fn apply_film_grain(
    base64_img: String,
    intensity: f32,
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

    // 使用简单的 LCG 随机数生成器
    let mut rng_state = 12345u32;

    for y in 0..height {
        for x in 0..width {
            let pixel = img.get_pixel(x, y);

            // 计算亮度（用于调制颗粒强度）
            let luminance = (0.299 * pixel[0] as f32 + 0.587 * pixel[1] as f32 + 0.114 * pixel[2] as f32) / 255.0;

            // 中间调颗粒更强（模拟真实胶片特性）
            let modulation = 1.0 - ((luminance - 0.5).abs() * 2.0).powf(0.8);

            // 生成高频随机噪声（替代 Perlin）
            rng_state = rng_state.wrapping_mul(1664525).wrapping_add(1013904223);
            let grain_r = ((rng_state as f32 / u32::MAX as f32) - 0.5) * 2.0;

            rng_state = rng_state.wrapping_mul(1664525).wrapping_add(1013904223);
            let grain_g = ((rng_state as f32 / u32::MAX as f32) - 0.5) * 2.0;

            rng_state = rng_state.wrapping_mul(1664525).wrapping_add(1013904223);
            let grain_b = ((rng_state as f32 / u32::MAX as f32) - 0.5) * 2.0;

            // 应用颗粒（带亮度调制和通道微偏移）
            let grain_strength = intensity * 25.0 * modulation;

            let r = (pixel[0] as f32 + grain_r * grain_strength).clamp(0.0, 255.0) as u8;
            let g = (pixel[1] as f32 + grain_g * grain_strength).clamp(0.0, 255.0) as u8;
            let b = (pixel[2] as f32 + grain_b * grain_strength).clamp(0.0, 255.0) as u8;

            result.put_pixel(x, y, Rgb([r, g, b]));
        }
    }

    encode_to_base64(&result)
}

// 辅助函数：盒模糊（快速近似高斯模糊）
fn apply_box_blur(img: &RgbImage, radius: u32) -> RgbImage {
    if radius == 0 {
        return img.clone();
    }

    let (width, height) = img.dimensions();
    let mut result = img.clone();
    let mut temp: RgbImage = ImageBuffer::new(width, height);

    let radius = radius.min(50); // 限制最大半径

    // 水平模糊
    for y in 0..height {
        for x in 0..width {
            let mut r_sum = 0u32;
            let mut g_sum = 0u32;
            let mut b_sum = 0u32;
            let mut count = 0u32;

            let x_start = x.saturating_sub(radius);
            let x_end = (x + radius + 1).min(width);

            for xx in x_start..x_end {
                let pixel = img.get_pixel(xx, y);
                r_sum += pixel[0] as u32;
                g_sum += pixel[1] as u32;
                b_sum += pixel[2] as u32;
                count += 1;
            }

            temp.put_pixel(x, y, Rgb([
                (r_sum / count) as u8,
                (g_sum / count) as u8,
                (b_sum / count) as u8,
            ]));
        }
    }

    // 垂直模糊
    for y in 0..height {
        for x in 0..width {
            let mut r_sum = 0u32;
            let mut g_sum = 0u32;
            let mut b_sum = 0u32;
            let mut count = 0u32;

            let y_start = y.saturating_sub(radius);
            let y_end = (y + radius + 1).min(height);

            for yy in y_start..y_end {
                let pixel = temp.get_pixel(x, yy);
                r_sum += pixel[0] as u32;
                g_sum += pixel[1] as u32;
                b_sum += pixel[2] as u32;
                count += 1;
            }

            result.put_pixel(x, y, Rgb([
                (r_sum / count) as u8,
                (g_sum / count) as u8,
                (b_sum / count) as u8,
            ]));
        }
    }

    result
}

// 辅助函数：添加白噪声
fn add_white_noise(img: &mut RgbImage, intensity: f32) {
    let (width, height) = img.dimensions();
    let mut rng_state = 54321u32;

    for y in 0..height {
        for x in 0..width {
            let pixel = img.get_pixel_mut(x, y);

            // 生成白噪声
            rng_state = rng_state.wrapping_mul(1664525).wrapping_add(1013904223);
            let noise = ((rng_state as f32 / u32::MAX as f32) - 0.5) * 2.0 * intensity * 20.0;

            pixel[0] = (pixel[0] as f32 + noise).clamp(0.0, 255.0) as u8;
            pixel[1] = (pixel[1] as f32 + noise).clamp(0.0, 255.0) as u8;
            pixel[2] = (pixel[2] as f32 + noise).clamp(0.0, 255.0) as u8;
        }
    }
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
