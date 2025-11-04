"""
Fruit Ninja Game with Hand Tracking
Slice fruits with your hand gestures!
"""
import cv2
import numpy as np
import random
import math
from typing import List, Tuple, Optional
import time
import os

from utils.landmark_extractor import LandmarkExtractor
from utils.image_loader import FruitImageLoader


class Fruit:
    """Represents a fruit in the game"""
    
    def __init__(self, fruit_type: str, x: float, speed: float, size: float = 50, 
                 image_loader: FruitImageLoader = None):
        """
        Initialize a fruit
        
        Args:
            fruit_type: Type of fruit (apple, banana, orange, etc.)
            x: Starting x position
            speed: Falling speed
            size: Fruit size
            image_loader: FruitImageLoader instance for getting fruit images
        """
        self.type = fruit_type
        self.x = x
        self.y = -size  # Start above screen
        self.speed = speed
        self.size = size
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.sliced = False
        self.score_value = 10 if fruit_type in ['apple', 'orange'] else 15
        
        # Store image loader reference
        self.image_loader = image_loader
        self.base_image = None
        
        # Load fruit image if image loader is provided
        if image_loader:
            self.base_image = image_loader.get_image(fruit_type)
        
    def update(self, dt: float):
        """Update fruit position"""
        if not self.sliced:
            self.y += self.speed * dt
            self.rotation += self.rotation_speed
            
    def draw(self, frame: np.ndarray):
        """Draw the fruit on the frame"""
        if self.sliced:
            return
        
        if self.base_image is not None and self.image_loader:
            # Use image
            # Resize image
            img_size = int(self.size * 2)
            resized_img = self.image_loader.resize_image(self.base_image, img_size)
            
            # Rotate image
            rotated_img = self.image_loader.rotate_image(resized_img, self.rotation)
            
            # Calculate position to draw (center the image)
            h, w = rotated_img.shape[:2]
            x1 = int(self.x - w // 2)
            y1 = int(self.y - h // 2)
            x2 = x1 + w
            y2 = y1 + h
            
            # Check bounds
            frame_h, frame_w = frame.shape[:2]
            
            # Calculate source region
            src_x1 = max(0, -x1)
            src_y1 = max(0, -y1)
            src_x2 = min(w, frame_w - x1)
            src_y2 = min(h, frame_h - y1)
            
            # Calculate destination region
            dst_x1 = max(0, x1)
            dst_y1 = max(0, y1)
            dst_x2 = min(frame_w, x2)
            dst_y2 = min(frame_h, y2)
            
            if dst_x2 > dst_x1 and dst_y2 > dst_y1 and src_x2 > src_x1 and src_y2 > src_y1:
                # Extract region from rotated image
                src_region = rotated_img[src_y1:src_y2, src_x1:src_x2]
                
                if src_region.shape[2] == 4:  # Has alpha channel
                    # Blend with alpha channel
                    alpha = src_region[:, :, 3:4] / 255.0
                    rgb = src_region[:, :, :3]
                    frame_region = frame[dst_y1:dst_y2, dst_x1:dst_x2]
                    blended = (rgb * alpha + frame_region * (1 - alpha)).astype(np.uint8)
                    frame[dst_y1:dst_y2, dst_x1:dst_x2] = blended
                else:
                    # No alpha channel, just copy
                    frame[dst_y1:dst_y2, dst_x1:dst_x2] = src_region
        else:
            # Fallback to circle if no image
            center = (int(self.x), int(self.y))
            color = (0, 0, 255) if self.type == 'apple' else (0, 200, 255)
            cv2.circle(frame, center, int(self.size), color, -1)
            cv2.circle(frame, center, int(self.size), (255, 255, 255), 2)
    
    def is_off_screen(self, height: int) -> bool:
        """Check if fruit is off screen"""
        return self.y > height + self.size
    
    def get_bounds(self) -> Tuple[int, int, int, int]:
        """Get bounding box (x, y, width, height)"""
        return (int(self.x - self.size), int(self.y - self.size),
                int(self.size * 2), int(self.size * 2))


class SliceDetector:
    """Detects slicing gestures from hand movement"""
    
    def __init__(self, min_slice_speed: float = 100.0):
        """
        Initialize slice detector
        
        Args:
            min_slice_speed: Minimum speed (pixels per frame) to register as a slice
        """
        self.min_slice_speed = min_slice_speed
        self.prev_landmarks = None
        self.prev_time = None
        
    def detect_slice(self, landmarks: Optional[np.ndarray]) -> Tuple[bool, Tuple[int, int], Tuple[int, int]]:
        """
        Detect if a slicing motion occurred
        
        Args:
            landmarks: Current hand landmarks
            
        Returns:
            Tuple of (is_slice, start_point, end_point)
        """
        if landmarks is None:
            self.prev_landmarks = None
            self.prev_time = None
            return False, None, None
        
        current_time = time.time()
        
        # Get index finger tip position (landmark 8)
        # Landmarks are stored as [x, y, z, x, y, z, ...]
        # Landmark 8 (index finger tip) is at indices 24-26
        if len(landmarks) < 27:
            return False, None, None
        
        current_x = landmarks[24]  # x coordinate
        current_y = landmarks[25]   # y coordinate
        
        # Convert normalized coordinates to pixel coordinates (assuming 640x480 default)
        # We'll use a fixed frame size for now
        frame_width = 640
        frame_height = 480
        
        current_px = int(current_x * frame_width)
        current_py = int(current_y * frame_height)
        
        if self.prev_landmarks is None or self.prev_time is None:
            self.prev_landmarks = landmarks.copy()
            self.prev_time = current_time
            return False, None, None
        
        prev_x = self.prev_landmarks[24]
        prev_y = self.prev_landmarks[25]
        prev_px = int(prev_x * frame_width)
        prev_py = int(prev_y * frame_height)
        
        # Calculate speed
        dt = current_time - self.prev_time
        if dt > 0:
            distance = math.sqrt((current_px - prev_px)**2 + (current_py - prev_py)**2)
            speed = distance / dt
            
            if speed > self.min_slice_speed:
                self.prev_landmarks = landmarks.copy()
                self.prev_time = current_time
                return True, (prev_px, prev_py), (current_px, current_py)
        
        self.prev_landmarks = landmarks.copy()
        self.prev_time = current_time
        return False, None, None
    
    def get_hand_path(self, landmarks: Optional[np.ndarray], frame_width: int, frame_height: int) -> List[Tuple[int, int]]:
        """
        Get current hand position for drawing trail
        
        Args:
            landmarks: Hand landmarks
            frame_width: Frame width
            frame_height: Frame height
            
        Returns:
            List of (x, y) positions
        """
        if landmarks is None or len(landmarks) < 27:
            return []
        
        # Get index finger tip
        x = int(landmarks[24] * frame_width)
        y = int(landmarks[25] * frame_height)
        
        return [(x, y)]


class FruitNinja:
    """Main Fruit Ninja game class"""
    
    def __init__(self, width: int = 640, height: int = 480):
        """
        Initialize Fruit Ninja game
        
        Args:
            width: Game window width
            height: Game window height
        """
        self.width = width
        self.height = height
        self.score = 0
        self.lives = 3
        self.game_over = False
        
        self.fruits: List[Fruit] = []
        self.fruit_types = ['apple', 'banana', 'orange', 'watermelon', 'pineapple']
        
        # Load fruit images
        self.image_loader = FruitImageLoader()
        
        self.landmark_extractor = LandmarkExtractor()
        self.slice_detector = SliceDetector(min_slice_speed=150.0)
        
        self.last_fruit_spawn = time.time()
        self.spawn_interval = 1.5  # Spawn a fruit every 1.5 seconds
        self.fruit_speed_range = (100, 200)  # Pixels per second
        
        self.slice_trail: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
        self.trail_max_length = 10
        self.hand_path: List[Tuple[int, int]] = []
        self.hand_path_max_length = 20
        
    def spawn_fruit(self):
        """Spawn a new fruit at random position"""
        if time.time() - self.last_fruit_spawn > self.spawn_interval:
            fruit_type = random.choice(self.fruit_types)
            x = random.randint(50, self.width - 50)
            speed = random.uniform(*self.fruit_speed_range)
            
            fruit = Fruit(fruit_type, x, speed, size=random.randint(40, 60), 
                         image_loader=self.image_loader)
            self.fruits.append(fruit)
            self.last_fruit_spawn = time.time()
            
            # Increase difficulty over time
            self.spawn_interval = max(0.5, 1.5 - self.score / 1000)
    
    def check_slice(self, start: Tuple[int, int], end: Tuple[int, int]) -> int:
        """
        Check if a slice intersects any fruits
        
        Args:
            start: Start point of slice
            end: End point of slice
            
        Returns:
            Number of fruits sliced
        """
        sliced_count = 0
        
        for fruit in self.fruits:
            if fruit.sliced:
                continue
            
            # Check if slice line intersects fruit circle
            if self.line_circle_intersect(start, end, 
                                         (int(fruit.x), int(fruit.y)), 
                                         int(fruit.size)):
                fruit.sliced = True
                self.score += fruit.score_value
                sliced_count += 1
        
        return sliced_count
    
    def line_circle_intersect(self, p1: Tuple[int, int], p2: Tuple[int, int],
                             center: Tuple[int, int], radius: int) -> bool:
        """
        Check if a line segment intersects a circle
        
        Args:
            p1: Start point of line
            p2: End point of line
            center: Circle center
            radius: Circle radius
            
        Returns:
            True if line intersects circle
        """
        # Vector from p1 to p2
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        
        # Vector from p1 to circle center
        fx = p1[0] - center[0]
        fy = p1[1] - center[1]
        
        # Calculate discriminant
        a = dx * dx + dy * dy
        b = 2 * (fx * dx + fy * dy)
        c = fx * fx + fy * fy - radius * radius
        
        discriminant = b * b - 4 * a * c
        
        if discriminant < 0:
            return False
        
        # Check if intersection point is on the line segment
        t1 = (-b - math.sqrt(discriminant)) / (2 * a)
        t2 = (-b + math.sqrt(discriminant)) / (2 * a)
        
        return (0 <= t1 <= 1) or (0 <= t2 <= 1)
    
    def update(self, frame: np.ndarray, dt: float):
        """
        Update game state
        
        Args:
            frame: Current camera frame
            dt: Delta time since last frame
        """
        if self.game_over:
            return
        
        # Extract hand landmarks
        landmarks, annotated_frame = self.landmark_extractor.process_frame(frame)
        
        # Detect slicing motion
        is_slice, slice_start, slice_end = self.slice_detector.detect_slice(landmarks)
        
        # Get hand position for trail
        hand_positions = self.slice_detector.get_hand_path(landmarks, self.width, self.height)
        if hand_positions:
            current_pos = hand_positions[0]
            
            # Add to hand path trail
            if len(self.hand_path) == 0 or self.hand_path[-1] != current_pos:
                self.hand_path.append(current_pos)
                if len(self.hand_path) > self.hand_path_max_length:
                    self.hand_path.pop(0)
            
            # Draw hand trail (fading effect)
            for i in range(len(self.hand_path) - 1):
                alpha = i / len(self.hand_path)
                color = (int(255 * alpha), 0, int(255 * (1 - alpha)))
                cv2.line(annotated_frame, self.hand_path[i], self.hand_path[i+1],
                        color, 2)
        
        if is_slice and slice_start and slice_end:
            # Draw white knife slash with glowing effect
            # Outer glow (thicker, slightly transparent would be ideal but using brighter white)
            cv2.line(annotated_frame, slice_start, slice_end, (255, 255, 255), 8)
            # Main slash line
            cv2.line(annotated_frame, slice_start, slice_end, (255, 255, 255), 6)
            # Inner bright line
            cv2.line(annotated_frame, slice_start, slice_end, (255, 255, 255), 4)
            
            # Add to slice trail
            self.slice_trail.append((slice_start, slice_end))
            if len(self.slice_trail) > self.trail_max_length:
                self.slice_trail.pop(0)
            
            # Check for fruit slices
            sliced = self.check_slice(slice_start, slice_end)
            if sliced > 0:
                # Add visual feedback for successful slice with white flash
                cv2.circle(annotated_frame, slice_end, 25, (255, 255, 255), -1)
                cv2.circle(annotated_frame, slice_end, 30, (255, 255, 255), 2)
        
        # Draw slice trail (white with fade out effect)
        for i, (start, end) in enumerate(self.slice_trail):
            alpha = (len(self.slice_trail) - i) / len(self.slice_trail) if self.slice_trail else 1
            # White color with alpha fade
            brightness = int(255 * alpha)
            color = (brightness, brightness, brightness)
            thickness = max(2, int(4 * alpha))
            cv2.line(annotated_frame, start, end, color, thickness)
        
        # Update fruits
        self.spawn_fruit()
        
        for fruit in self.fruits[:]:
            fruit.update(dt)
            fruit.draw(annotated_frame)
            
            # Remove fruits that are off screen or sliced
            if fruit.is_off_screen(self.height):
                if not fruit.sliced:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_over = True
                self.fruits.remove(fruit)
            elif fruit.sliced:
                # Keep sliced fruits for a moment, then remove
                if time.time() - getattr(fruit, 'sliced_time', time.time()) > 0.1:
                    self.fruits.remove(fruit)
                else:
                    if not hasattr(fruit, 'sliced_time'):
                        fruit.sliced_time = time.time()
        
        # Draw UI
        self.draw_ui(annotated_frame)
        
        return annotated_frame
    
    def draw_ui(self, frame: np.ndarray):
        """Draw game UI (score, lives, etc.)"""
        # Draw score
        score_text = f"Score: {self.score}"
        cv2.putText(frame, score_text, (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Draw lives
        lives_text = f"Lives: {self.lives}"
        cv2.putText(frame, lives_text, (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        # Draw game over
        if self.game_over:
            game_over_text = "GAME OVER! Press 'r' to restart"
            text_size = cv2.getTextSize(game_over_text, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            text_x = (self.width - text_size[0]) // 2
            text_y = (self.height + text_size[1]) // 2
            cv2.putText(frame, game_over_text, (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    def reset(self):
        """Reset game state"""
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.fruits.clear()
        self.last_fruit_spawn = time.time()
        self.spawn_interval = 1.5
        self.hand_path.clear()
        self.slice_trail.clear()


def main():
    """Main game loop"""
    print("Fruit Ninja - Hand Tracking Edition")
    print("Instructions:")
    print("- Move your hand quickly to slice fruits")
    print("- Don't let fruits fall to the bottom!")
    print("- Press 'q' to quit, 'r' to restart")
    print("\nStarting game...")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set camera resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    game = FruitNinja(width=640, height=480)
    
    prev_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            
            # Calculate delta time
            current_time = time.time()
            dt = current_time - prev_time
            prev_time = current_time
            
            # Update game
            game_frame = game.update(frame, dt)
            
            # Display frame
            cv2.imshow("Fruit Ninja", game_frame)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                game.reset()
                print("Game restarted!")
    
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print(f"\nFinal Score: {game.score}")


if __name__ == "__main__":
    main()

