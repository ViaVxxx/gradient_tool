"""Favorites management for saving and organizing gradient images."""
import os
import json
from datetime import datetime
from typing import List, Dict, Any
from PIL import Image
import hashlib


class FavoritesManager:
    """Manages favorite gradient images."""

    def __init__(self, favorites_dir: str = "favorites"):
        """Initialize favorites manager.
        
        Args:
            favorites_dir: Directory to store favorite images and metadata
        """
        self.favorites_dir = favorites_dir
        self.metadata_file = os.path.join(favorites_dir, "metadata.json")
        self.thumbnails_dir = os.path.join(favorites_dir, "thumbnails")
        self.images_dir = os.path.join(favorites_dir, "images")
        
        # Create directories if they don't exist
        os.makedirs(self.thumbnails_dir, exist_ok=True)
        os.makedirs(self.images_dir, exist_ok=True)
        
        # Load existing metadata
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> Dict[str, Any]:
        """Load metadata from file."""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                pass
        return {"favorites": []}

    def _save_metadata(self):
        """Save metadata to file."""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, indent=2, ensure_ascii=False)
        except IOError:
            pass

    def _generate_id(self, image: Image.Image, gradient_state) -> str:
        """Generate unique ID for a gradient based on its properties."""
        # Create a hash based on gradient properties
        properties = {
            'type': gradient_state.gradient_type,
            'angle': gradient_state.angle,
            'stops': [(s.position, s.color.to_hex()) for s in gradient_state.stops],
            'noise': gradient_state.noise_intensity,
            'vignette': gradient_state.vignette_intensity,
            'width': gradient_state.width,
            'height': gradient_state.height
        }
        
        properties_str = json.dumps(properties, sort_keys=True)
        return hashlib.md5(properties_str.encode()).hexdigest()[:12]

    def add_favorite(self, image: Image.Image, gradient_state, name: str = None) -> str:
        """Add image to favorites.
        
        Args:
            image: PIL Image to save
            gradient_state: Current gradient state
            name: Optional custom name
            
        Returns:
            ID of the saved favorite
        """
        favorite_id = self._generate_id(image, gradient_state)
        
        # Check if already exists
        if any(fav['id'] == favorite_id for fav in self.metadata['favorites']):
            return favorite_id
        
        # Generate name if not provided
        if not name:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"渐变_{timestamp}"
        
        # Save full image
        image_path = os.path.join(self.images_dir, f"{favorite_id}.png")
        image.save(image_path, 'PNG')
        
        # Create and save thumbnail (120x120)
        thumbnail = image.copy()
        thumbnail.thumbnail((120, 120), Image.LANCZOS)
        thumbnail_path = os.path.join(self.thumbnails_dir, f"{favorite_id}.png")
        thumbnail.save(thumbnail_path, 'PNG')
        
        # Add to metadata
        favorite_data = {
            'id': favorite_id,
            'name': name,
            'created_at': datetime.now().isoformat(),
            'gradient_type': gradient_state.gradient_type,
            'angle': gradient_state.angle,
            'stops': [(s.position, s.color.to_hex()) for s in gradient_state.stops],
            'noise_intensity': gradient_state.noise_intensity,
            'vignette_intensity': gradient_state.vignette_intensity,
            'width': gradient_state.width,
            'height': gradient_state.height,
            'image_path': image_path,
            'thumbnail_path': thumbnail_path
        }
        
        self.metadata['favorites'].append(favorite_data)
        self._save_metadata()
        
        return favorite_id

    def remove_favorite(self, favorite_id: str) -> bool:
        """Remove favorite by ID.
        
        Args:
            favorite_id: ID of favorite to remove
            
        Returns:
            True if removed, False if not found
        """
        for i, fav in enumerate(self.metadata['favorites']):
            if fav['id'] == favorite_id:
                # Remove files
                try:
                    if os.path.exists(fav['image_path']):
                        os.remove(fav['image_path'])
                    if os.path.exists(fav['thumbnail_path']):
                        os.remove(fav['thumbnail_path'])
                except OSError:
                    pass
                
                # Remove from metadata
                self.metadata['favorites'].pop(i)
                self._save_metadata()
                return True
        return False

    def get_favorites(self) -> List[Dict[str, Any]]:
        """Get list of all favorites."""
        return self.metadata['favorites'].copy()

    def get_favorite(self, favorite_id: str) -> Dict[str, Any]:
        """Get specific favorite by ID."""
        for fav in self.metadata['favorites']:
            if fav['id'] == favorite_id:
                return fav.copy()
        return None

    def get_thumbnail_path(self, favorite_id: str) -> str:
        """Get thumbnail path for favorite."""
        fav = self.get_favorite(favorite_id)
        if fav and os.path.exists(fav['thumbnail_path']):
            return fav['thumbnail_path']
        return None

    def get_image_path(self, favorite_id: str) -> str:
        """Get full image path for favorite."""
        fav = self.get_favorite(favorite_id)
        if fav and os.path.exists(fav['image_path']):
            return fav['image_path']
        return None

    def export_favorites(self, favorite_ids: List[str], export_dir: str, format: str = 'png') -> List[str]:
        """Export multiple favorites to directory.
        
        Args:
            favorite_ids: List of favorite IDs to export
            export_dir: Directory to export to
            format: Export format ('png' or 'jpg')
            
        Returns:
            List of exported file paths
        """
        os.makedirs(export_dir, exist_ok=True)
        exported_files = []
        
        for fav_id in favorite_ids:
            fav = self.get_favorite(fav_id)
            if not fav:
                continue
                
            # Load original image
            try:
                image = Image.open(fav['image_path'])
                
                # Generate export filename
                safe_name = "".join(c for c in fav['name'] if c.isalnum() or c in (' ', '-', '_')).strip()
                filename = f"{safe_name}_{fav_id}.{format}"
                export_path = os.path.join(export_dir, filename)
                
                # Save in requested format
                if format.lower() == 'jpg':
                    if image.mode == 'RGBA':
                        # Convert to RGB for JPEG
                        background = Image.new('RGB', image.size, (255, 255, 255))
                        background.paste(image, mask=image.split()[3] if len(image.split()) == 4 else None)
                        image = background
                    image.save(export_path, 'JPEG', quality=95)
                else:
                    image.save(export_path, 'PNG')
                
                exported_files.append(export_path)
                
            except (IOError, OSError):
                continue
        
        return exported_files