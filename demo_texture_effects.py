#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
纹理效果演示脚本
展示新增的磨砂质感、噪点、沙砾等效果
"""

from PIL import Image
from core.gradient_engine import GradientEngine
from core.color_utils import Color, ColorStop
from core.effects import Effects
import os

def create_demo_gradients():
    """创建演示渐变图像"""

    print("正在生成纹理效果演示图像...")

    # 创建输出目录
    output_dir = "texture_demos"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 创建渐变引擎
    engine = GradientEngine(800, 600)

    # 定义基础渐变
    stops = [
        ColorStop(0.0, Color.from_hex("#667EEA")),
        ColorStop(0.5, Color.from_hex("#764BA2")),
        ColorStop(1.0, Color.from_hex("#F093FB"))
    ]

    # 1. 原始渐变（无效果）
    print("1. 生成原始渐变...")
    base_gradient = engine.render_linear_gradient(stops, angle=135)
    base_gradient.save(f"{output_dir}/01_base_gradient.png")
    print(f"   保存: {output_dir}/01_base_gradient.png")

    # 2. 基础噪点效果
    print("2. 生成基础噪点效果...")
    with_noise = Effects.apply_noise(base_gradient, intensity=0.15, grain_size=1)
    with_noise.save(f"{output_dir}/02_basic_noise.png")
    print(f"   保存: {output_dir}/02_basic_noise.png")

    # 3. Perlin噪点（更自然）
    print("3. 生成Perlin噪点（自然纹理）...")
    with_perlin = Effects.apply_perlin_noise(base_gradient, intensity=0.2, scale=50, octaves=3)
    with_perlin.save(f"{output_dir}/03_perlin_noise.png")
    print(f"   保存: {output_dir}/03_perlin_noise.png")

    # 4. 磨砂玻璃效果
    print("4. 生成磨砂玻璃效果...")
    frosted = Effects.apply_frosted_glass(base_gradient, intensity=0.25, grain_size=2.5)
    frosted.save(f"{output_dir}/04_frosted_glass.png")
    print(f"   保存: {output_dir}/04_frosted_glass.png")

    # 5. 沙砾质感
    print("5. 生成沙砾质感...")
    granular = Effects.apply_granular_texture(base_gradient, intensity=0.3, grain_size=2, coverage=0.8)
    granular.save(f"{output_dir}/05_granular_texture.png")
    print(f"   保存: {output_dir}/05_granular_texture.png")

    # 6. 胶片颗粒
    print("6. 生成胶片颗粒效果...")
    film = Effects.apply_film_grain(base_gradient, intensity=0.25, grain_size=2)
    film.save(f"{output_dir}/06_film_grain.png")
    print(f"   保存: {output_dir}/06_film_grain.png")

    # 7. 多层噪点（丰富纹理）
    print("7. 生成多层噪点...")
    layered = Effects.apply_layered_noise(base_gradient, layers=3, base_intensity=0.18)
    layered.save(f"{output_dir}/07_layered_noise.png")
    print(f"   保存: {output_dir}/07_layered_noise.png")

    # 8. 组合效果：磨砂玻璃 + 晕影
    print("8. 生成组合效果（磨砂玻璃+晕影）...")
    frosted_vig = Effects.apply_frosted_glass(base_gradient, intensity=0.2, grain_size=2.0)
    frosted_vig = Effects.apply_vignette(frosted_vig, intensity=0.4, spread=0.6)
    frosted_vig.save(f"{output_dir}/08_frosted_vignette.png")
    print(f"   保存: {output_dir}/08_frosted_vignette.png")

    # 9. 组合效果：沙砾 + Perlin噪点
    print("9. 生成组合效果（沙砾+Perlin）...")
    combo = Effects.apply_granular_texture(base_gradient, intensity=0.25, grain_size=1, coverage=0.7)
    combo = Effects.apply_perlin_noise(combo, intensity=0.1, scale=40, octaves=2)
    combo.save(f"{output_dir}/09_granular_perlin.png")
    print(f"   保存: {output_dir}/09_granular_perlin.png")

    # 10. 超强质感组合
    print("10. 生成超强质感组合...")
    ultra = Effects.apply_perlin_noise(base_gradient, intensity=0.15, scale=35, octaves=4)
    ultra = Effects.apply_granular_texture(ultra, intensity=0.2, grain_size=2, coverage=0.6)
    ultra = Effects.apply_vignette(ultra, intensity=0.35, spread=0.65)
    ultra.save(f"{output_dir}/10_ultra_texture.png")
    print(f"   保存: {output_dir}/10_ultra_texture.png")

    print(f"\n✅ 完成！所有演示图像已保存到 '{output_dir}' 目录")
    print(f"\n📊 生成的效果对比：")
    print("   01 - 原始渐变（参考）")
    print("   02 - 基础噪点（简单随机噪点）")
    print("   03 - Perlin噪点（自然纹理，推荐！）")
    print("   04 - 磨砂玻璃（模糊+细腻噪点）")
    print("   05 - 沙砾质感（粗糙颗粒感）")
    print("   06 - 胶片颗粒（复古胶片效果）")
    print("   07 - 多层噪点（丰富层次感）")
    print("   08 - 磨砂+晕影（优雅组合）")
    print("   09 - 沙砾+Perlin（粗糙自然）")
    print("   10 - 超强质感（终极组合！）")

    print(f"\n💡 提示：")
    print("   - 在主应用中，你可以在'纹理效果'面板选择这些效果")
    print("   - 调整'效果强度'和'颗粒大小'可以微调效果")
    print("   - 不同效果适合不同的设计风格，尝试找到最适合你的！")


if __name__ == "__main__":
    create_demo_gradients()
