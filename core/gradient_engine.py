"""Gradient rendering engine using PIL."""
from typing import List, Tuple
from PIL import Image, ImageDraw
import math
from .color_utils import Color, ColorStop, generate_gradient_colors


class GradientType:
    """Gradient type constants."""
    LINEAR = "linear"
    RADIAL = "radial"
    CONIC = "conic"


class GradientEngine:
    """Core gradient rendering engine."""

    def __init__(self, width: int = 800, height: int = 600):
        """Initialize gradient engine.

        Args:
            width: Image width in pixels
            height: Image height in pixels
        """
        self.width = width
        self.height = height
        self.image = None

    def render_linear_gradient(self,
                              stops: List[ColorStop],
                              angle: float = 0,
                              color_space: str = 'rgb') -> Image.Image:
        """Render linear gradient.

        Args:
            stops: Color stops for the gradient
            angle: Angle in degrees (0 = left to right, 90 = top to bottom)
            color_space: Color space for interpolation

        Returns:
            PIL Image with rendered gradient
        """
        # Create new image
        image = Image.new('RGB', (self.width, self.height))

        # Convert angle to radians
        angle_rad = math.radians(angle)

        # Calculate gradient direction vector
        dx = math.cos(angle_rad)
        dy = math.sin(angle_rad)

        # Calculate the projection bounds
        # Project all four corners onto the gradient line
        corners = [
            (0, 0),
            (self.width, 0),
            (0, self.height),
            (self.width, self.height)
        ]

        projections = [x * dx + y * dy for x, y in corners]
        min_proj = min(projections)
        max_proj = max(projections)
        proj_range = max_proj - min_proj

        # Generate color lookup table
        colors = generate_gradient_colors(stops, 256, color_space)

        # Render pixel by pixel
        pixels = image.load()

        for y in range(self.height):
            for x in range(self.width):
                # Project point onto gradient line
                proj = x * dx + y * dy

                # Normalize to 0-1 range
                t = (proj - min_proj) / proj_range if proj_range > 0 else 0
                t = max(0, min(1, t))

                # Get color from lookup table
                color_idx = int(t * 255)
                color = colors[color_idx]

                pixels[x, y] = color.to_rgb()

        self.image = image
        return image

    def render_radial_gradient(self,
                               stops: List[ColorStop],
                               center_x: float = 0.5,
                               center_y: float = 0.5,
                               radius: float = 0.5,
                               color_space: str = 'rgb') -> Image.Image:
        """Render radial gradient.

        Args:
            stops: Color stops for the gradient
            center_x: Center X position (0.0-1.0)
            center_y: Center Y position (0.0-1.0)
            radius: Radius (0.0-1.0, relative to image diagonal)
            color_space: Color space for interpolation

        Returns:
            PIL Image with rendered gradient
        """
        # Create new image
        image = Image.new('RGB', (self.width, self.height))

        # Calculate center position in pixels
        cx = self.width * center_x
        cy = self.height * center_y

        # Calculate radius in pixels (relative to diagonal)
        diagonal = math.sqrt(self.width ** 2 + self.height ** 2)
        r = diagonal * radius

        # Generate color lookup table
        colors = generate_gradient_colors(stops, 256, color_space)

        # Render pixel by pixel
        pixels = image.load()

        for y in range(self.height):
            for x in range(self.width):
                # Calculate distance from center
                dist = math.sqrt((x - cx) ** 2 + (y - cy) ** 2)

                # Normalize to 0-1 range
                t = dist / r if r > 0 else 0
                t = max(0, min(1, t))

                # Get color from lookup table
                color_idx = int(t * 255)
                color = colors[color_idx]

                pixels[x, y] = color.to_rgb()

        self.image = image
        return image

    def get_image(self) -> Image.Image:
        """Get the current rendered image."""
        return self.image

    def resize(self, width: int, height: int):
        """Resize the rendering canvas."""
        self.width = width
        self.height = height
