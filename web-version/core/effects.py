"""Image effects system (noise, vignette, etc.)."""
from PIL import Image, ImageFilter, ImageDraw
import random
import math


class PerlinNoise:
    """简化的Perlin噪声生成器"""

    def __init__(self, seed=None):
        if seed is not None:
            random.seed(seed)

        # 生成置换表
        self.p = list(range(256))
        random.shuffle(self.p)
        self.p *= 2

    def fade(self, t):
        """平滑曲线"""
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, t, a, b):
        """线性插值"""
        return a + t * (b - a)

    def grad(self, hash_val, x, y):
        """梯度函数"""
        h = hash_val & 3
        u = x if h < 2 else y
        v = y if h < 2 else x
        return (u if (h & 1) == 0 else -u) + (v if (h & 2) == 0 else -v)

    def noise(self, x, y):
        """生成Perlin噪声值"""
        # 找到单位正方形
        X = int(x) & 255
        Y = int(y) & 255

        # 找到相对位置
        x -= int(x)
        y -= int(y)

        # 计算淡入曲线
        u = self.fade(x)
        v = self.fade(y)

        # 哈希坐标
        a = self.p[X] + Y
        aa = self.p[a]
        ab = self.p[a + 1]
        b = self.p[X + 1] + Y
        ba = self.p[b]
        bb = self.p[b + 1]

        # 插值结果
        return self.lerp(v,
                        self.lerp(u, self.grad(self.p[aa], x, y),
                                 self.grad(self.p[ba], x - 1, y)),
                        self.lerp(u, self.grad(self.p[ab], x, y - 1),
                                 self.grad(self.p[bb], x - 1, y - 1)))


class Effects:
    """Image effects processor."""

    @staticmethod
    def apply_noise(image: Image.Image, intensity: float = 0.1,
                   grain_size: int = 1) -> Image.Image:
        """Apply noise/grain effect to image."""
        width, height = image.size
        pixels = image.load()
        noisy_image = image.copy()
        noisy_pixels = noisy_image.load()
        noise_range = int(255 * intensity)

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                r = max(0, min(255, r + random.randint(-noise_range, noise_range)))
                g = max(0, min(255, g + random.randint(-noise_range, noise_range)))
                b = max(0, min(255, b + random.randint(-noise_range, noise_range)))
                noisy_pixels[x, y] = (r, g, b)

        if grain_size > 1:
            noisy_image = noisy_image.filter(ImageFilter.GaussianBlur(radius=grain_size * 0.3))
        return noisy_image

    @staticmethod
    def apply_perlin_noise(image: Image.Image, intensity: float = 0.15,
                          scale: float = 50.0, octaves: int = 3) -> Image.Image:
        """Apply Perlin noise for natural texture."""
        width, height = image.size
        pixels = image.load()
        perlin = PerlinNoise(seed=random.randint(0, 10000))
        noise_map = {}

        for y in range(height):
            for x in range(width):
                noise_val = 0
                amplitude = 1.0
                frequency = 1.0
                max_val = 0

                for _ in range(octaves):
                    nx = x / scale * frequency
                    ny = y / scale * frequency
                    noise_val += perlin.noise(nx, ny) * amplitude
                    max_val += amplitude
                    amplitude *= 0.5
                    frequency *= 2.0

                noise_val /= max_val
                noise_map[(x, y)] = noise_val

        result = image.copy()
        result_pixels = result.load()

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                noise = noise_map[(x, y)] * intensity * 255
                r = int(max(0, min(255, r + noise)))
                g = int(max(0, min(255, g + noise)))
                b = int(max(0, min(255, b + noise)))
                result_pixels[x, y] = (r, g, b)

        return result

    @staticmethod
    def apply_frosted_glass(image: Image.Image, intensity: float = 0.2,
                           grain_size: float = 2.0) -> Image.Image:
        """Apply frosted glass effect (blur + noise)."""
        blurred = image.filter(ImageFilter.GaussianBlur(radius=grain_size * 0.8))
        with_noise = Effects.apply_perlin_noise(blurred, intensity=intensity * 0.6, scale=30)
        with_grain = Effects.apply_noise(with_noise, intensity=intensity * 0.3, grain_size=1)
        return with_grain

    @staticmethod
    def apply_granular_texture(image: Image.Image, intensity: float = 0.25,
                              grain_size: int = 2, coverage: float = 0.7) -> Image.Image:
        """Apply granular/sandy texture."""
        width, height = image.size
        pixels = image.load()
        result = image.copy()
        result_pixels = result.load()

        for y in range(height):
            for x in range(width):
                if random.random() < coverage:
                    r, g, b = pixels[x, y]
                    grain_offset = random.randint(-int(intensity * 255), int(intensity * 255))
                    r = max(0, min(255, r + grain_offset))
                    g = max(0, min(255, g + grain_offset + random.randint(-10, 10)))
                    b = max(0, min(255, b + grain_offset + random.randint(-10, 10)))
                    result_pixels[x, y] = (r, g, b)

        if grain_size > 1:
            result = result.filter(ImageFilter.GaussianBlur(radius=grain_size * 0.2))
        return result

    @staticmethod
    def apply_film_grain(image: Image.Image, intensity: float = 0.2,
                        grain_size: int = 2) -> Image.Image:
        """Apply film grain effect."""
        perlin_result = Effects.apply_perlin_noise(image, intensity=intensity * 0.6, scale=40)
        final = Effects.apply_noise(perlin_result, intensity=intensity * 0.4, grain_size=grain_size)
        return final

    @staticmethod
    def apply_layered_noise(image: Image.Image, layers: int = 3,
                           base_intensity: float = 0.15) -> Image.Image:
        """Apply multiple layers of noise for rich texture."""
        result = image.copy()
        for i in range(layers):
            scale = 30 + i * 20
            intensity = base_intensity * (1.0 - i * 0.25)
            result = Effects.apply_perlin_noise(result, intensity=intensity, scale=scale, octaves=2)
        return result

    @staticmethod
    def apply_vignette(image: Image.Image, intensity: float = 0.5,
                      spread: float = 0.5) -> Image.Image:
        """Apply vignette effect (edge darkening)."""
        width, height = image.size
        mask = Image.new('L', (width, height), 255)
        mask_pixels = mask.load()
        cx, cy = width / 2, height / 2
        max_dist = math.sqrt(cx ** 2 + cy ** 2)

        for y in range(height):
            for x in range(width):
                dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)
                norm_dist = dist / max_dist
                adjusted_dist = (norm_dist - spread) / (1 - spread) if spread < 1 else 0
                adjusted_dist = max(0, min(1, adjusted_dist))
                vignette_value = int((1 - (adjusted_dist * intensity)) * 255)
                mask_pixels[x, y] = vignette_value

        result = Image.new('RGB', (width, height))
        result_pixels = result.load()
        img_pixels = image.load()

        for y in range(height):
            for x in range(width):
                r, g, b = img_pixels[x, y]
                factor = mask_pixels[x, y] / 255
                result_pixels[x, y] = (int(r * factor), int(g * factor), int(b * factor))

        return result

    @staticmethod
    def apply_blur(image: Image.Image, radius: float = 2.0) -> Image.Image:
        """Apply Gaussian blur effect."""
        return image.filter(ImageFilter.GaussianBlur(radius=radius))
