"""
Gradient Tool - Web 版本主入口
使用 PyWebView 桥接 Python 后端和 Vue 前端
"""
import webview
from pathlib import Path

class API:
    """暴露给前端的 Python API"""

    def __init__(self):
        # 导入现有的核心模块
        from core.gradient_engine import GradientEngine
        from core.effects import Effects
        from core.presets import PresetLibrary
        from core.color_utils import Color, ColorStop

        self.engine = GradientEngine(800, 600)
        self.effects = Effects
        self.presets = PresetLibrary()
        self.current_image = None
        self.original_image = None  # 保存原始渐变图像

        # 保存类引用供方法使用
        self.Color = Color
        self.ColorStop = ColorStop

    def generate_gradient(self, gradient_type, stops, angle=0, center_x=0.5, center_y=0.5):
        """生成渐变图像"""
        try:
            # 转换 stops 数据
            color_stops = []
            for stop in stops:
                color = self.Color(stop['color']['r'], stop['color']['g'], stop['color']['b'])
                color_stops.append(self.ColorStop(stop['position'], color))

            # 生成渐变
            if gradient_type == 'linear':
                image = self.engine.render_linear_gradient(color_stops, angle)
            else:  # radial
                image = self.engine.render_radial_gradient(color_stops, center_x, center_y)

            self.current_image = image
            self.original_image = image.copy()  # 保存原始图像副本

            # 转换为 base64 返回给前端
            import io
            import base64
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            return {
                'success': True,
                'image': f'data:image/png;base64,{img_str}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def apply_effect(self, effect_type, intensity=0.2):
        """应用纹理效果"""
        if not self.original_image:
            return {'success': False, 'error': 'No image generated'}

        try:
            # 如果强度为0，直接返回原始图像
            if intensity == 0:
                result = self.original_image.copy()
            else:
                # 从原始图像应用效果
                if effect_type == 'perlin':
                    result = self.effects.apply_perlin_noise(self.original_image, intensity)
                elif effect_type == 'frosted':
                    result = self.effects.apply_frosted_glass(self.original_image, intensity)
                elif effect_type == 'film':
                    result = self.effects.apply_film_grain(self.original_image, intensity)
                elif effect_type == 'vignette':
                    result = self.effects.apply_vignette(self.original_image, intensity)
                else:
                    return {'success': False, 'error': 'Unknown effect type'}

            self.current_image = result

            # 转换为 base64
            import io
            import base64
            buffered = io.BytesIO()
            result.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            return {
                'success': True,
                'image': f'data:image/png;base64,{img_str}'
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def get_presets(self, category=None):
        """获取预设列表"""
        if category:
            presets = self.presets.get_by_category(category)
        else:
            presets = self.presets.presets

        # 转换为前端友好的格式
        result = []
        for preset in presets:
            result.append({
                'name': preset.name,
                'category': preset.category,
                'gradient_type': preset.gradient_type,
                'angle': preset.angle,
                'stops': [
                    {
                        'position': stop.position,
                        'color': {
                            'r': stop.color.r,
                            'g': stop.color.g,
                            'b': stop.color.b
                        }
                    }
                    for stop in preset.stops
                ]
            })
        return result

    def export_image(self, format='png', quality=95):
        """导出图像"""
        if not self.current_image:
            return {'success': False, 'error': 'No image to export'}

        try:
            from utils.export import ExportManager
            from datetime import datetime

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'gradient_{timestamp}.{format}'

            if format == 'png':
                filepath = ExportManager.export_png(self.current_image, filename)
            else:
                filepath = ExportManager.export_jpg(self.current_image, filename, quality)

            return {
                'success': True,
                'filepath': filepath
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }


def main():
    """启动应用"""
    api = API()

    # 获取前端文件路径
    web_dir = Path(__file__).parent / 'web' / 'dist'

    # 开发模式：使用 Vite 开发服务器
    # 生产模式：使用构建后的文件
    if web_dir.exists():
        # 生产模式
        window = webview.create_window(
            'Gradient Tool',
            str(web_dir / 'index.html'),
            js_api=api,
            width=1600,
            height=900,
            resizable=True,
            frameless=False
        )
    else:
        # 开发模式 - 连接到 Vite 开发服务器
        window = webview.create_window(
            'Gradient Tool',
            'http://localhost:5173',
            js_api=api,
            width=1600,
            height=900,
            resizable=True,
            frameless=False
        )

    webview.start(debug=True)


if __name__ == '__main__':
    main()
