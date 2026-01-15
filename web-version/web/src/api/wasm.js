import init, {
  GradientEngine,
  apply_perlin_noise,
  apply_vignette,
  apply_frosted_glass,
  apply_film_grain,
} from '../wasm-pkg/gradient_wasm.js';

let wasmReady = null;
let engine = null;

export async function initWasm() {
  if (!wasmReady) {
    wasmReady = init();
    await wasmReady;
    engine = new GradientEngine(800, 600);
  }
  return engine;
}

export async function generateGradient(type, stops, angle = 0, cx = 0.5, cy = 0.5) {
  await initWasm();

  try {
    let base64;
    if (type === 'linear') {
      base64 = engine.render_linear(stops, angle);
    } else {
      base64 = engine.render_radial(stops, cx, cy);
    }
    return { success: true, image: `data:image/png;base64,${base64}` };
  } catch (error) {
    console.error('WASM gradient generation error:', error);
    return { success: false, error: error.toString() };
  }
}

export async function applyEffect(type, intensity, currentImage) {
  await initWasm();

  try {
    // 从 data URL 提取 base64
    const base64 = currentImage.split(',')[1];

    let result;
    switch (type) {
      case 'perlin':
        result = apply_perlin_noise(base64, intensity, 50.0, 3);
        break;
      case 'vignette':
        result = apply_vignette(base64, intensity, 0.5);
        break;
      case 'frosted':
        result = apply_frosted_glass(base64, intensity);
        break;
      case 'film':
        result = apply_film_grain(base64, intensity);
        break;
      default:
        throw new Error(`Unknown effect type: ${type}`);
    }

    return { success: true, image: `data:image/png;base64,${result}` };
  } catch (error) {
    console.error('WASM effect application error:', error);
    return { success: false, error: error.toString() };
  }
}
