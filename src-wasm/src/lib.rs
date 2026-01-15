mod color;
mod gradient;
mod effects;

pub use color::{Color, ColorStop};
pub use gradient::GradientEngine;
pub use effects::{apply_perlin_noise, apply_vignette, apply_frosted_glass, apply_film_grain};

use wasm_bindgen::prelude::*;

#[wasm_bindgen(start)]
pub fn main() {
    // 设置 panic hook 以便在浏览器控制台看到错误
    #[cfg(feature = "console_error_panic_hook")]
    console_error_panic_hook::set_once();
}
