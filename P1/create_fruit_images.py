"""
Create simple fruit images for the game
You can replace these with actual fruit images later
"""
import cv2
import numpy as np
from pathlib import Path


def create_fruit_image(fruit_type: str, size: int = 100):
    """
    Create a colorful fruit image
    
    Args:
        fruit_type: Type of fruit
        size: Image size
    """
    # Create image with alpha channel
    img = np.zeros((size, size, 4), dtype=np.uint8)
    
    # Colors and patterns for different fruits
    center = (size // 2, size // 2)
    
    if fruit_type == 'apple':
        # Red apple with green leaf
        cv2.circle(img, center, size // 2 - 5, (0, 0, 255, 255), -1)  # Red
        cv2.circle(img, center, size // 2 - 5, (255, 255, 255, 255), 2)  # Outline
        # Stem
        cv2.ellipse(img, (center[0], center[1] - size // 3), (5, 10), 0, 0, 180, (50, 50, 50, 255), -1)
        # Leaf
        cv2.ellipse(img, (center[0] + 5, center[1] - size // 3 - 5), (8, 12), 45, 0, 360, (0, 150, 0, 255), -1)
    
    elif fruit_type == 'banana':
        # Yellow banana
        cv2.ellipse(img, center, (size // 2 - 5, size // 3), 45, 0, 360, (0, 200, 255, 255), -1)
        cv2.ellipse(img, center, (size // 2 - 5, size // 3), 45, 0, 360, (255, 255, 255, 255), 2)
    
    elif fruit_type == 'orange':
        # Orange fruit
        cv2.circle(img, center, size // 2 - 5, (0, 165, 255, 255), -1)  # Orange
        cv2.circle(img, center, size // 2 - 5, (255, 255, 255, 255), 2)
        # Add some texture lines
        for i in range(4):
            angle = i * 90
            start_x = center[0] + int(20 * np.cos(np.radians(angle)))
            start_y = center[1] + int(20 * np.sin(np.radians(angle)))
            end_x = center[0] + int(35 * np.cos(np.radians(angle)))
            end_y = center[1] + int(35 * np.sin(np.radians(angle)))
            cv2.line(img, (start_x, start_y), (end_x, end_y), (0, 140, 230, 200), 1)
    
    elif fruit_type == 'watermelon':
        # Green watermelon
        cv2.circle(img, center, size // 2 - 5, (0, 100, 0, 255), -1)  # Green
        cv2.circle(img, center, size // 2 - 5, (255, 255, 255, 255), 2)
        # Add stripes
        for i in range(0, size, 8):
            cv2.line(img, (0, i), (size, i), (0, 120, 0, 200), 1)
    
    elif fruit_type == 'pineapple':
        # Yellow pineapple
        cv2.circle(img, center, size // 2 - 5, (0, 200, 255, 255), -1)  # Yellow
        cv2.circle(img, center, size // 2 - 5, (255, 255, 255, 255), 2)
        # Add diamond pattern
        for i in range(-30, 40, 15):
            for j in range(-30, 40, 15):
                if (i + j) % 30 == 0:
                    cv2.circle(img, (center[0] + i, center[1] + j), 3, (0, 180, 230, 255), -1)
    
    else:
        # Default circle
        cv2.circle(img, center, size // 2 - 5, (255, 255, 255, 255), -1)
        cv2.circle(img, center, size // 2 - 5, (255, 255, 255, 255), 2)
    
    return img


def main():
    """Create all fruit images"""
    assets_dir = Path("assets/fruits")
    assets_dir.mkdir(parents=True, exist_ok=True)
    
    fruit_types = ['apple', 'banana', 'orange', 'watermelon', 'pineapple']
    size = 120  # Larger size for better quality
    
    print("Creating fruit images...")
    
    for fruit_type in fruit_types:
        img = create_fruit_image(fruit_type, size)
        output_path = assets_dir / f"{fruit_type}.png"
        cv2.imwrite(str(output_path), img)
        print(f"Created: {fruit_type}.png")
    
    print(f"\nAll fruit images created in {assets_dir}/")
    print("You can replace these with actual fruit images if you have them!")


if __name__ == "__main__":
    main()

