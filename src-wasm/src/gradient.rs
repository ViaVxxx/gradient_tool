use crate::color::{Color, ColorStop};
use image::{ImageBuffer, Rgb, RgbImage};
use wasm_bindgen::prelude::*;
use std::io::Cursor;
use base64::{Engine as _, engine::general_purpose};

#[wasm_bindgen]
pub struct GradientEngine {
    width: u32,
    height: u32,
}

#[wasm_bindgen]
impl GradientEngine {
    #[wasm_bindgen(constructor)]
    pub fn new(width: u32, height: u32) -> Self {
        Self { width, height }
    }

    pub fn render_linear(&self, stops_js: JsValue, angle: f32) -> Result<String, JsValue> {
        // 解析色标
        let stops: Vec<ColorStop> = serde_wasm_bindgen::from_value(stops_js)
            .map_err(|e| JsValue::from_str(&format!("Failed to parse stops: {:?}", e)))?;

        if stops.len() < 2 {
            return Err(JsValue::from_str("At least 2 color stops required"));
        }

        // 创建图像缓冲区
        let mut img: RgbImage = ImageBuffer::new(self.width, self.height);

        // 计算渐变方向向量
        let angle_rad = angle.to_radians();
        let dx = angle_rad.cos();
        let dy = angle_rad.sin();

        // 计算投影范围
        let corners = [
            (0.0, 0.0),
            (self.width as f32, 0.0),
            (0.0, self.height as f32),
            (self.width as f32, self.height as f32),
        ];

        let mut min_proj = f32::MAX;
        let mut max_proj = f32::MIN;

        for (x, y) in corners.iter() {
            let proj = x * dx + y * dy;
            min_proj = min_proj.min(proj);
            max_proj = max_proj.max(proj);
        }

        let range = max_proj - min_proj;

        // 生成颜色查找表 (LUT)
        let lut = Self::generate_lut(&stops, 256);

        // 逐像素填充
        for y in 0..self.height {
            for x in 0..self.width {
                let proj = x as f32 * dx + y as f32 * dy;
                let t = ((proj - min_proj) / range).clamp(0.0, 1.0);
                let idx = (t * 255.0) as usize;
                let color = lut[idx];
                img.put_pixel(x, y, Rgb([color.r, color.g, color.b]));
            }
        }

        // 编码为 PNG Base64
        Self::encode_to_base64(&img)
    }

    pub fn render_radial(&self, stops_js: JsValue, cx: f32, cy: f32) -> Result<String, JsValue> {
        // 解析色标
        let stops: Vec<ColorStop> = serde_wasm_bindgen::from_value(stops_js)
            .map_err(|e| JsValue::from_str(&format!("Failed to parse stops: {:?}", e)))?;

        if stops.len() < 2 {
            return Err(JsValue::from_str("At least 2 color stops required"));
        }

        // 创建图像缓冲区
        let mut img: RgbImage = ImageBuffer::new(self.width, self.height);

        // 计算中心点和最大半径
        let center_x = cx * self.width as f32;
        let center_y = cy * self.height as f32;
        let max_radius = ((self.width as f32 / 2.0).powi(2) + (self.height as f32 / 2.0).powi(2)).sqrt();

        // 生成颜色查找表
        let lut = Self::generate_lut(&stops, 256);

        // 逐像素填充
        for y in 0..self.height {
            for x in 0..self.width {
                let dx = x as f32 - center_x;
                let dy = y as f32 - center_y;
                let distance = (dx * dx + dy * dy).sqrt();
                let t = (distance / max_radius).clamp(0.0, 1.0);
                let idx = (t * 255.0) as usize;
                let color = lut[idx];
                img.put_pixel(x, y, Rgb([color.r, color.g, color.b]));
            }
        }

        // 编码为 PNG Base64
        Self::encode_to_base64(&img)
    }
}

impl GradientEngine {
    fn generate_lut(stops: &[ColorStop], size: usize) -> Vec<Color> {
        let mut lut = Vec::with_capacity(size);

        for i in 0..size {
            let t = i as f32 / (size - 1) as f32;

            // 找到当前位置对应的两个色标
            let mut left_stop = &stops[0];
            let mut right_stop = &stops[stops.len() - 1];

            for j in 0..stops.len() - 1 {
                if t >= stops[j].position && t <= stops[j + 1].position {
                    left_stop = &stops[j];
                    right_stop = &stops[j + 1];
                    break;
                }
            }

            // 插值
            let local_t = if right_stop.position == left_stop.position {
                0.0
            } else {
                (t - left_stop.position) / (right_stop.position - left_stop.position)
            };

            let color = Color::interpolate_rgb(&left_stop.color, &right_stop.color, local_t);
            lut.push(color);
        }

        lut
    }

    fn encode_to_base64(img: &RgbImage) -> Result<String, JsValue> {
        let mut buffer = Cursor::new(Vec::new());
        img.write_to(&mut buffer, image::ImageOutputFormat::Png)
            .map_err(|e| JsValue::from_str(&format!("Failed to encode PNG: {:?}", e)))?;

        let base64_str = general_purpose::STANDARD.encode(buffer.into_inner());
        Ok(base64_str)
    }
}
