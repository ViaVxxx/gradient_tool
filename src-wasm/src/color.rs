use serde::{Deserialize, Serialize};
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
#[derive(Debug, Clone, Copy, Serialize, Deserialize)]
pub struct Color {
    pub r: u8,
    pub g: u8,
    pub b: u8,
}

#[wasm_bindgen]
impl Color {
    #[wasm_bindgen(constructor)]
    pub fn new(r: u8, g: u8, b: u8) -> Self {
        Self { r, g, b }
    }

    pub fn from_hex(hex: &str) -> Result<Color, JsValue> {
        let hex = hex.trim_start_matches('#');
        if hex.len() != 6 {
            return Err(JsValue::from_str("Invalid hex color format"));
        }

        let r = u8::from_str_radix(&hex[0..2], 16)
            .map_err(|_| JsValue::from_str("Invalid hex color"))?;
        let g = u8::from_str_radix(&hex[2..4], 16)
            .map_err(|_| JsValue::from_str("Invalid hex color"))?;
        let b = u8::from_str_radix(&hex[4..6], 16)
            .map_err(|_| JsValue::from_str("Invalid hex color"))?;

        Ok(Color { r, g, b })
    }

    pub fn to_hex(&self) -> String {
        format!("#{:02x}{:02x}{:02x}", self.r, self.g, self.b)
    }

    pub fn to_hsl(&self) -> Vec<f32> {
        let r = self.r as f32 / 255.0;
        let g = self.g as f32 / 255.0;
        let b = self.b as f32 / 255.0;

        let max = r.max(g).max(b);
        let min = r.min(g).min(b);
        let delta = max - min;

        let l = (max + min) / 2.0;

        if delta == 0.0 {
            return vec![0.0, 0.0, l];
        }

        let s = if l < 0.5 {
            delta / (max + min)
        } else {
            delta / (2.0 - max - min)
        };

        let h = if max == r {
            ((g - b) / delta + if g < b { 6.0 } else { 0.0 }) / 6.0
        } else if max == g {
            ((b - r) / delta + 2.0) / 6.0
        } else {
            ((r - g) / delta + 4.0) / 6.0
        };

        vec![h * 360.0, s, l]
    }

    pub fn from_hsl(h: f32, s: f32, l: f32) -> Color {
        let h = h / 360.0;

        if s == 0.0 {
            let gray = (l * 255.0) as u8;
            return Color { r: gray, g: gray, b: gray };
        }

        let q = if l < 0.5 {
            l * (1.0 + s)
        } else {
            l + s - l * s
        };
        let p = 2.0 * l - q;

        let r = Self::hue_to_rgb(p, q, h + 1.0 / 3.0);
        let g = Self::hue_to_rgb(p, q, h);
        let b = Self::hue_to_rgb(p, q, h - 1.0 / 3.0);

        Color {
            r: (r * 255.0) as u8,
            g: (g * 255.0) as u8,
            b: (b * 255.0) as u8,
        }
    }
}

impl Color {
    fn hue_to_rgb(p: f32, q: f32, mut t: f32) -> f32 {
        if t < 0.0 {
            t += 1.0;
        }
        if t > 1.0 {
            t -= 1.0;
        }
        if t < 1.0 / 6.0 {
            return p + (q - p) * 6.0 * t;
        }
        if t < 1.0 / 2.0 {
            return q;
        }
        if t < 2.0 / 3.0 {
            return p + (q - p) * (2.0 / 3.0 - t) * 6.0;
        }
        p
    }

    pub fn interpolate_rgb(c1: &Color, c2: &Color, t: f32) -> Color {
        let t = t.clamp(0.0, 1.0);
        Color {
            r: (c1.r as f32 + (c2.r as f32 - c1.r as f32) * t) as u8,
            g: (c1.g as f32 + (c2.g as f32 - c1.g as f32) * t) as u8,
            b: (c1.b as f32 + (c2.b as f32 - c1.b as f32) * t) as u8,
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ColorStop {
    pub position: f32,
    pub color: Color,
}

impl ColorStop {
    pub fn new(position: f32, color: Color) -> Self {
        Self { position, color }
    }
}
