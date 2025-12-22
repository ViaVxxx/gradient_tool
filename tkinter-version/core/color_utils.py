"""Color utility functions for gradient generation."""
from typing import Tuple, List
import colorsys


class Color:
    """Represents a color with multiple format support."""

    def __init__(self, r: int = 0, g: int = 0, b: int = 0, a: int = 255):
        """Initialize color with RGBA values (0-255)."""
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        self.a = max(0, min(255, a))

    @classmethod
    def from_hex(cls, hex_color: str) -> 'Color':
        """Create color from hex string (#RRGGBB or #RGB)."""
        hex_color = hex_color.lstrip('#')

        if len(hex_color) == 3:
            hex_color = ''.join([c*2 for c in hex_color])

        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: {hex_color}")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        return cls(r, g, b)

    @classmethod
    def from_hsl(cls, h: float, s: float, l: float) -> 'Color':
        """Create color from HSL values (H: 0-360, S: 0-100, L: 0-100)."""
        h_norm = h / 360.0
        s_norm = s / 100.0
        l_norm = l / 100.0

        r, g, b = colorsys.hls_to_rgb(h_norm, l_norm, s_norm)

        return cls(int(r * 255), int(g * 255), int(b * 255))

    def to_hex(self) -> str:
        """Convert to hex string."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def to_rgb(self) -> Tuple[int, int, int]:
        """Convert to RGB tuple."""
        return (self.r, self.g, self.b)

    def to_rgba(self) -> Tuple[int, int, int, int]:
        """Convert to RGBA tuple."""
        return (self.r, self.g, self.b, self.a)

    def to_hsl(self) -> Tuple[float, float, float]:
        """Convert to HSL tuple (H: 0-360, S: 0-100, L: 0-100)."""
        r_norm = self.r / 255.0
        g_norm = self.g / 255.0
        b_norm = self.b / 255.0

        h, l, s = colorsys.rgb_to_hls(r_norm, g_norm, b_norm)

        return (h * 360, s * 100, l * 100)

    def __repr__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"


class ColorStop:
    """Represents a color stop in a gradient."""

    def __init__(self, position: float, color: Color):
        """Initialize color stop.

        Args:
            position: Position in gradient (0.0-1.0)
            color: Color at this position
        """
        self.position = max(0.0, min(1.0, position))
        self.color = color

    def __repr__(self) -> str:
        return f"ColorStop(pos={self.position:.2f}, color={self.color.to_hex()})"


def interpolate_color(color1: Color, color2: Color, t: float,
                     color_space: str = 'rgb') -> Color:
    """Interpolate between two colors.

    Args:
        color1: Start color
        color2: End color
        t: Interpolation factor (0.0-1.0)
        color_space: Color space for interpolation ('rgb', 'hsl')

    Returns:
        Interpolated color
    """
    t = max(0.0, min(1.0, t))

    if color_space == 'rgb':
        r = int(color1.r + (color2.r - color1.r) * t)
        g = int(color1.g + (color2.g - color1.g) * t)
        b = int(color1.b + (color2.b - color1.b) * t)
        a = int(color1.a + (color2.a - color1.a) * t)
        return Color(r, g, b, a)

    elif color_space == 'hsl':
        h1, s1, l1 = color1.to_hsl()
        h2, s2, l2 = color2.to_hsl()

        # Handle hue interpolation (shortest path around color wheel)
        dh = h2 - h1
        if dh > 180:
            dh -= 360
        elif dh < -180:
            dh += 360

        h = (h1 + dh * t) % 360
        s = s1 + (s2 - s1) * t
        l = l1 + (l2 - l1) * t

        return Color.from_hsl(h, s, l)

    else:
        raise ValueError(f"Unknown color space: {color_space}")


def generate_gradient_colors(stops: List[ColorStop], steps: int,
                            color_space: str = 'rgb') -> List[Color]:
    """Generate a list of interpolated colors from color stops.

    Args:
        stops: List of color stops (must be sorted by position)
        steps: Number of color steps to generate
        color_space: Color space for interpolation

    Returns:
        List of interpolated colors
    """
    if len(stops) < 2:
        raise ValueError("At least 2 color stops required")

    # Sort stops by position
    stops = sorted(stops, key=lambda s: s.position)

    colors = []

    for i in range(steps):
        t = i / (steps - 1) if steps > 1 else 0

        # Find the two stops to interpolate between
        stop1, stop2 = stops[0], stops[-1]

        for j in range(len(stops) - 1):
            if stops[j].position <= t <= stops[j + 1].position:
                stop1, stop2 = stops[j], stops[j + 1]
                break

        # Calculate local interpolation factor
        if stop2.position - stop1.position > 0:
            local_t = (t - stop1.position) / (stop2.position - stop1.position)
        else:
            local_t = 0

        color = interpolate_color(stop1.color, stop2.color, local_t, color_space)
        colors.append(color)

    return colors
