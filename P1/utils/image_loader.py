"""
Utility for loading and managing fruit images
"""
import cv2
import numpy as np
from pathlib import Path
from typing import Dict, Optional
import os


class FruitImageLoader:
    """Loads and manages fruit images"""
    
    def __init__(self, assets_dir: str = "assets/fruits"):
        """
        Initialize image loader
        
        Args:
            assets_dir: Directory containing fruit images
        """
        self.assets_dir = Path(assets_dir)
        self.images: Dict[str, np.ndarray] = {}
        self.fruit_types = ['apple', 'banana', 'orange', 'watermelon', 'pineapple']
        self.load_images()
    
    def load_images(self):
        """Load all fruit images from assets directory"""
        # Create directory if it doesn't exist
        self.assets_dir.mkdir(parents=True, exist_ok=True)
        
        # Try to load images, if not found, create placeholder images
        for fruit_type in self.fruit_types:
            image_path = self.assets_dir / f"{fruit_type}.png"
            
            if image_path.exists():
                img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
                if img is not None:
                    self.images[fruit_type] = img
                    print(f"Loaded image: {fruit_type}.png")
                else:
                    self.images[fruit_type] = self._create_placeholder(fruit_type)
            else:
                # Create a placeholder image if file doesn't exist
                self.images[fruit_type] = self._create_placeholder(fruit_type)
                self._save_placeholder(fruit_type, self.images[fruit_type])
    
    def _create_placeholder(self, fruit_type: str, size: int = 100) -> np.ndarray:
        """
        Create a simple colored circle placeholder for fruit
        
        Args:
            fruit_type: Type of fruit
            size: Size of the placeholder image
            
        Returns:
            Image array with alpha channel
        """
        # Create image with alpha channel
        img = np.zeros((size, size, 4), dtype=np.uint8)
        
        # Colors for different fruits
        colors = {
            'apple': (0, 0, 255, 255),      # Red
            'banana': (0, 200, 255, 255),    # Yellow
            'orange': (0, 165, 255, 255),    # Orange
            'watermelon': (0, 100, 0, 255),  # Green
            'pineapple': (0, 200, 255, 255), # Yellow
        }
        
        color = colors.get(fruit_type, (255, 255, 255, 255))
        center = (size // 2, size // 2)
        radius = size // 2 - 5
        
        # Draw filled circle
        cv2.circle(img, center, radius, color, -1)
        
        # Draw outline
        cv2.circle(img, center, radius, (255, 255, 255, 255), 2)
        
        # Add text
        text = fruit_type[:3].upper()
        text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
        text_x = center[0] - text_size[0] // 2
        text_y = center[1] + text_size[1] // 2
        cv2.putText(img, text, (text_x, text_y),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255, 255), 2)
        
        return img
    
    def _save_placeholder(self, fruit_type: str, img: np.ndarray):
        """Save placeholder image to file"""
        output_path = self.assets_dir / f"{fruit_type}.png"
        cv2.imwrite(str(output_path), img)
        print(f"Created placeholder image: {fruit_type}.png")
    
    def get_image(self, fruit_type: str) -> Optional[np.ndarray]:
        """
        Get image for a fruit type
        
        Args:
            fruit_type: Type of fruit
            
        Returns:
            Image array or None if not found
        """
        return self.images.get(fruit_type)
    
    def rotate_image(self, img: np.ndarray, angle: float) -> np.ndarray:
        """
        Rotate image by given angle
        
        Args:
            img: Input image
            angle: Rotation angle in degrees
            
        Returns:
            Rotated image
        """
        if len(img.shape) == 3 and img.shape[2] == 4:
            # Image has alpha channel
            h, w = img.shape[:2]
            center = (w // 2, h // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # Calculate new dimensions to avoid cropping
            cos = np.abs(rotation_matrix[0, 0])
            sin = np.abs(rotation_matrix[0, 1])
            new_w = int((h * sin) + (w * cos))
            new_h = int((h * cos) + (w * sin))
            
            # Adjust rotation matrix for new dimensions
            rotation_matrix[0, 2] += (new_w / 2) - center[0]
            rotation_matrix[1, 2] += (new_h / 2) - center[1]
            
            rotated = cv2.warpAffine(img, rotation_matrix, (new_w, new_h),
                                   flags=cv2.INTER_LINEAR,
                                   borderMode=cv2.BORDER_TRANSPARENT)
            return rotated
        else:
            # No alpha channel, standard rotation
            h, w = img.shape[:2]
            center = (w // 2, h // 2)
            rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            rotated = cv2.warpAffine(img, rotation_matrix, (w, h),
                                   flags=cv2.INTER_LINEAR,
                                   borderMode=cv2.BORDER_CONSTANT,
                                   borderValue=(0, 0, 0))
            return rotated
    
    def resize_image(self, img: np.ndarray, size: int) -> np.ndarray:
        """
        Resize image to given size
        
        Args:
            img: Input image
            size: Target size (width and height)
            
        Returns:
            Resized image
        """
        return cv2.resize(img, (size, size), interpolation=cv2.INTER_LINEAR)

