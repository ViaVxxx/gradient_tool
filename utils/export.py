"""Export functionality for saving gradients."""
from PIL import Image
import os
from datetime import datetime
from typing import Tuple


class ExportManager:
    """Manages image export operations."""

    @staticmethod
    def export_png(image: Image.Image, filepath: str = None,
                  dpi: Tuple[int, int] = (72, 72)) -> str:
        """Export image as PNG.

        Args:
            image: PIL Image to export
            filepath: Output file path (auto-generated if None)
            dpi: DPI resolution tuple (x, y)

        Returns:
            Path to saved file
        """
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"gradient_{timestamp}.png"

        # Save with metadata
        image.save(filepath, 'PNG', dpi=dpi, optimize=True)

        return filepath

    @staticmethod
    def export_jpg(image: Image.Image, filepath: str = None,
                  quality: int = 95, dpi: Tuple[int, int] = (72, 72)) -> str:
        """Export image as JPG.

        Args:
            image: PIL Image to export
            filepath: Output file path (auto-generated if None)
            quality: JPEG quality (1-100)
            dpi: DPI resolution tuple (x, y)

        Returns:
            Path to saved file
        """
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = f"gradient_{timestamp}.jpg"

        # Convert RGBA to RGB if necessary
        if image.mode == 'RGBA':
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])  # Use alpha channel as mask
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        # Save with quality setting
        image.save(filepath, 'JPEG', quality=quality, dpi=dpi, optimize=True)

        return filepath

    @staticmethod
    def get_default_export_path(format: str = 'png') -> str:
        """Generate default export file path.

        Args:
            format: File format extension

        Returns:
            Generated file path
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"gradient_{timestamp}.{format}"
