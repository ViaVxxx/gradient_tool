#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速纹理效果应用工具
直接为你的渐变图像添加质感效果
"""

from PIL import Image
from core.effects import Effects
import sys
import os


def print_menu():
    """打印效果选择菜单"""
    print("\n" + "="*60)
    print("  渐变纹理效果快速应用工具")
    print("="*60)
    print("\n可用效果:")
    print("  1. Perlin噪点 (自然流畅，推荐)")
    print("  2. 磨砂玻璃 (优雅柔和)")
    print("  3. 沙砾质感 (粗糙颗粒)")
    print("  4. 胶片颗粒 (复古艺术)")
    print("  5. 多层噪点 (丰富层次)")
    print("  6. 磨砂+晕影组合 (优雅背景)")
    print("  7. 超强质感组合 (终极效果)")
    print("  8. 基础噪点 (快速简单)")
    print("  0. 退出")
    print("-"*60)


def apply_effect_interactive():
    """交互式应用效果"""

    # 1. 先生成一个演示渐变或让用户选择图像
    print("\n选择输入方式:")
    print("  1. 使用演示渐变 (自动生成)")
    print("  2. 选择自己的图像文件")

    choice = input("\n请输入选择 (1/2): ").strip()

    if choice == "1":
        # 生成演示渐变
        print("\n正在生成演示渐变...")
        from core.gradient_engine import GradientEngine
        from core.color_utils import Color, ColorStop

        engine = GradientEngine(800, 600)
        stops = [
            ColorStop(0.0, Color.from_hex("#667EEA")),
            ColorStop(0.5, Color.from_hex("#764BA2")),
            ColorStop(1.0, Color.from_hex("#F093FB"))
        ]
        image = engine.render_linear_gradient(stops, angle=135)
        print("演示渐变生成完成!")

    elif choice == "2":
        # 选择现有图像
        img_path = input("\n请输入图像文件路径: ").strip().strip('"')

        if not os.path.exists(img_path):
            print(f"错误: 文件不存在 - {img_path}")
            return

        try:
            image = Image.open(img_path)
            print(f"成功加载图像: {img_path}")
        except Exception as e:
            print(f"错误: 无法打开图像 - {e}")
            return
    else:
        print("无效选择!")
        return

    # 2. 选择效果
    while True:
        print_menu()
        effect_choice = input("请选择效果 (0-8): ").strip()

        if effect_choice == "0":
            print("\n再见!")
            break

        if effect_choice not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            print("无效选择，请重新输入!")
            continue

        # 应用效果
        print("\n正在应用效果，请稍候...")

        try:
            if effect_choice == "1":
                result = Effects.apply_perlin_noise(image, intensity=0.2, scale=50, octaves=3)
                effect_name = "perlin_noise"

            elif effect_choice == "2":
                result = Effects.apply_frosted_glass(image, intensity=0.2, grain_size=2.5)
                effect_name = "frosted_glass"

            elif effect_choice == "3":
                result = Effects.apply_granular_texture(image, intensity=0.3, grain_size=2, coverage=0.8)
                effect_name = "granular"

            elif effect_choice == "4":
                result = Effects.apply_film_grain(image, intensity=0.25, grain_size=2)
                effect_name = "film_grain"

            elif effect_choice == "5":
                result = Effects.apply_layered_noise(image, layers=3, base_intensity=0.18)
                effect_name = "layered_noise"

            elif effect_choice == "6":
                result = Effects.apply_frosted_glass(image, intensity=0.2, grain_size=2.0)
                result = Effects.apply_vignette(result, intensity=0.35, spread=0.65)
                effect_name = "frosted_vignette"

            elif effect_choice == "7":
                result = Effects.apply_perlin_noise(image, intensity=0.15, scale=35, octaves=4)
                result = Effects.apply_granular_texture(result, intensity=0.2, grain_size=2, coverage=0.6)
                result = Effects.apply_vignette(result, intensity=0.35, spread=0.65)
                effect_name = "ultra_texture"

            elif effect_choice == "8":
                result = Effects.apply_noise(image, intensity=0.15, grain_size=1)
                effect_name = "basic_noise"

            # 保存结果
            output_path = f"output_{effect_name}.png"
            result.save(output_path)
            print(f"\n成功! 图像已保存到: {output_path}")

            # 询问是否继续
            cont = input("\n是否继续应用其他效果? (y/n): ").strip().lower()
            if cont != 'y':
                print("\n完成! 感谢使用!")
                break

        except Exception as e:
            print(f"\n错误: 应用效果失败 - {e}")
            continue


def quick_apply(image_path, effect_type="perlin", intensity=0.2):
    """快速应用效果（命令行模式）"""

    if not os.path.exists(image_path):
        print(f"错误: 文件不存在 - {image_path}")
        return

    try:
        image = Image.open(image_path)
        print(f"加载图像: {image_path}")

        if effect_type == "perlin":
            result = Effects.apply_perlin_noise(image, intensity=intensity, scale=50)
        elif effect_type == "frosted":
            result = Effects.apply_frosted_glass(image, intensity=intensity)
        elif effect_type == "film":
            result = Effects.apply_film_grain(image, intensity=intensity)
        elif effect_type == "granular":
            result = Effects.apply_granular_texture(image, intensity=intensity)
        elif effect_type == "layered":
            result = Effects.apply_layered_noise(image, base_intensity=intensity)
        elif effect_type == "ultra":
            result = Effects.apply_perlin_noise(image, intensity=intensity)
            result = Effects.apply_granular_texture(result, intensity=intensity * 0.7)
        else:
            print(f"未知效果类型: {effect_type}")
            return

        output_path = f"output_{effect_type}.png"
        result.save(output_path)
        print(f"完成! 保存到: {output_path}")

    except Exception as e:
        print(f"错误: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 命令行模式
        image_path = sys.argv[1]
        effect_type = sys.argv[2] if len(sys.argv) > 2 else "perlin"
        intensity = float(sys.argv[3]) if len(sys.argv) > 3 else 0.2

        print(f"\n命令行模式:")
        print(f"  图像: {image_path}")
        print(f"  效果: {effect_type}")
        print(f"  强度: {intensity}")
        print()

        quick_apply(image_path, effect_type, intensity)

    else:
        # 交互模式
        apply_effect_interactive()
