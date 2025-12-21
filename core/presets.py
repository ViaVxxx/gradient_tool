"""Preset gradient library."""
from typing import List, Dict
from .color_utils import ColorStop, Color
from .gradient_engine import GradientType


class GradientPreset:
    """Represents a gradient preset."""

    def __init__(self, name: str, gradient_type: str, stops: List[ColorStop],
                 angle: float = 0, category: str = "Other", tags: List[str] = None):
        """Initialize preset.

        Args:
            name: Preset name
            gradient_type: Type of gradient (linear, radial, etc.)
            stops: Color stops
            angle: Angle for linear gradient
            category: Category name
            tags: List of tags
        """
        self.name = name
        self.gradient_type = gradient_type
        self.stops = stops
        self.angle = angle
        self.category = category
        self.tags = tags or []

    def to_dict(self) -> Dict:
        """Convert preset to dictionary."""
        return {
            'name': self.name,
            'type': self.gradient_type,
            'angle': self.angle,
            'category': self.category,
            'tags': self.tags,
            'stops': [
                {
                    'position': stop.position,
                    'color': stop.color.to_hex()
                }
                for stop in self.stops
            ]
        }


class PresetLibrary:
    """Preset library manager."""

    def __init__(self):
        """Initialize preset library."""
        self.presets: List[GradientPreset] = []
        self._load_default_presets()

    def _load_default_presets(self):
        """Load default preset collection."""

        # 1. Monochrome - Blue series
        self.add_preset(GradientPreset(
            name="Ocean Deep",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#001F3F")),
                ColorStop(1.0, Color.from_hex("#83B3D3"))
            ],
            angle=135,
            category="Monochrome",
            tags=["blue", "calm", "ocean"]
        ))

        self.add_preset(GradientPreset(
            name="Sky Blue",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#89CFF0")),
                ColorStop(1.0, Color.from_hex("#D4F1F4"))
            ],
            angle=90,
            category="Monochrome",
            tags=["blue", "light", "sky"]
        ))

        # 2. Warm-Cool Contrast
        self.add_preset(GradientPreset(
            name="Sunset Glow",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#FF6B35")),
                ColorStop(0.5, Color.from_hex("#F7931E")),
                ColorStop(1.0, Color.from_hex("#FDC830"))
            ],
            angle=45,
            category="Sunset",
            tags=["warm", "orange", "sunset"]
        ))

        self.add_preset(GradientPreset(
            name="Fire & Ice",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#FF0844")),
                ColorStop(1.0, Color.from_hex("#00D4FF"))
            ],
            angle=90,
            category="Warm-Cool",
            tags=["contrast", "vibrant"]
        ))

        # 3. Neon/Vibrant
        self.add_preset(GradientPreset(
            name="Neon Dreams",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#FF00FF")),
                ColorStop(0.5, Color.from_hex("#00FFFF")),
                ColorStop(1.0, Color.from_hex("#FFFF00"))
            ],
            angle=135,
            category="Neon",
            tags=["neon", "vibrant", "colorful"]
        ))

        # 4. Analogous Colors
        self.add_preset(GradientPreset(
            name="Purple Dreams",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#667EEA")),
                ColorStop(1.0, Color.from_hex("#764BA2"))
            ],
            angle=90,
            category="Analogous",
            tags=["purple", "smooth"]
        ))

        self.add_preset(GradientPreset(
            name="Forest Path",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#134E5E")),
                ColorStop(1.0, Color.from_hex("#71B280"))
            ],
            angle=135,
            category="Analogous",
            tags=["green", "nature"]
        ))

        # 5. Complementary
        self.add_preset(GradientPreset(
            name="Citrus Burst",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#FF6B35")),
                ColorStop(1.0, Color.from_hex("#004E89"))
            ],
            angle=45,
            category="Complementary",
            tags=["orange", "blue", "contrast"]
        ))

        # 6. Radial Glows
        self.add_preset(GradientPreset(
            name="Soft Glow",
            gradient_type=GradientType.RADIAL,
            stops=[
                ColorStop(0.0, Color.from_hex("#FFFFFF")),
                ColorStop(1.0, Color.from_hex("#E0E0E0"))
            ],
            category="Radial Glow",
            tags=["radial", "soft", "light"]
        ))

        self.add_preset(GradientPreset(
            name="Neon Center",
            gradient_type=GradientType.RADIAL,
            stops=[
                ColorStop(0.0, Color.from_hex("#FF00FF")),
                ColorStop(1.0, Color.from_hex("#000000"))
            ],
            category="Radial Glow",
            tags=["radial", "neon", "dark"]
        ))

        # 7. Muted/Morandi Colors
        self.add_preset(GradientPreset(
            name="Soft Peach",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#FFDAB9")),
                ColorStop(1.0, Color.from_hex("#FFE4E1"))
            ],
            angle=90,
            category="Muted",
            tags=["peach", "soft", "pastel"]
        ))

        self.add_preset(GradientPreset(
            name="Dusty Rose",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#C9ADA7")),
                ColorStop(1.0, Color.from_hex("#F2E9E4"))
            ],
            angle=135,
            category="Muted",
            tags=["rose", "muted", "elegant"]
        ))

        # 8. Triadic/Multi-color
        self.add_preset(GradientPreset(
            name="Rainbow Flow",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#FF0000")),
                ColorStop(0.33, Color.from_hex("#00FF00")),
                ColorStop(0.67, Color.from_hex("#0000FF")),
                ColorStop(1.0, Color.from_hex("#FF00FF"))
            ],
            angle=90,
            category="Triadic",
            tags=["rainbow", "colorful", "vibrant"]
        ))

        # 9. Aqua/Mint
        self.add_preset(GradientPreset(
            name="Mint Fresh",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#00F5A0")),
                ColorStop(1.0, Color.from_hex("#00D9F5"))
            ],
            angle=135,
            category="Aqua/Mint",
            tags=["mint", "fresh", "cyan"]
        ))

        self.add_preset(GradientPreset(
            name="Tropical Water",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#1E3A8A")),
                ColorStop(1.0, Color.from_hex("#06B6D4"))
            ],
            angle=90,
            category="Aqua/Mint",
            tags=["aqua", "tropical", "blue"]
        ))

        # 10. Earth Tones
        self.add_preset(GradientPreset(
            name="Desert Sand",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#C9A170")),
                ColorStop(1.0, Color.from_hex("#E8D5C4"))
            ],
            angle=45,
            category="Earth Tone",
            tags=["sand", "earth", "warm"]
        ))

        self.add_preset(GradientPreset(
            name="Forest Floor",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#5F4B32")),
                ColorStop(1.0, Color.from_hex("#9A7B4F"))
            ],
            angle=135,
            category="Earth Tone",
            tags=["brown", "earth", "natural"]
        ))

        # 11. Metallic
        self.add_preset(GradientPreset(
            name="Silver Shine",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#B0B0B0")),
                ColorStop(0.5, Color.from_hex("#E8E8E8")),
                ColorStop(1.0, Color.from_hex("#888888"))
            ],
            angle=90,
            category="Metallic",
            tags=["silver", "metallic", "shine"]
        ))

        self.add_preset(GradientPreset(
            name="Gold Gleam",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#C9A961")),
                ColorStop(0.5, Color.from_hex("#F4E4C1")),
                ColorStop(1.0, Color.from_hex("#B8922F"))
            ],
            angle=135,
            category="Metallic",
            tags=["gold", "metallic", "luxury"]
        ))

        # 12. Brand/UI backgrounds
        self.add_preset(GradientPreset(
            name="Modern UI Blue",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#3B82F6")),
                ColorStop(1.0, Color.from_hex("#1E40AF"))
            ],
            angle=135,
            category="Brand/UI",
            tags=["blue", "ui", "modern"]
        ))

        self.add_preset(GradientPreset(
            name="Success Green",
            gradient_type=GradientType.LINEAR,
            stops=[
                ColorStop(0.0, Color.from_hex("#10B981")),
                ColorStop(1.0, Color.from_hex("#059669"))
            ],
            angle=90,
            category="Brand/UI",
            tags=["green", "success", "ui"]
        ))

    def add_preset(self, preset: GradientPreset):
        """Add a preset to the library."""
        self.presets.append(preset)

    def get_presets(self, category: str = None) -> List[GradientPreset]:
        """Get presets, optionally filtered by category."""
        if category:
            return [p for p in self.presets if p.category == category]
        return self.presets

    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        return sorted(list(set(p.category for p in self.presets)))

    def get_preset_by_name(self, name: str) -> GradientPreset:
        """Get preset by name."""
        for preset in self.presets:
            if preset.name == name:
                return preset
        return None
