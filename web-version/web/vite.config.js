import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import wasm from 'vite-plugin-wasm'
import topLevelAwait from 'vite-plugin-top-level-await'

export default defineConfig({
  plugins: [
    vue(),
    wasm(),
    topLevelAwait(),
  ],
  server: {
    port: 5173,
    strictPort: true,
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    target: 'esnext', // WASM 需要
    minify: 'esbuild', // 比 terser 更快
  },
  resolve: {
    alias: {
      '@': '/src',
    },
  },
  // Tauri 配置
  clearScreen: false,
  envPrefix: ['VITE_', 'TAURI_'],
})
