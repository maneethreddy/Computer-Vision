"""
Landmark extraction utilities using MediaPipe
"""
import cv2
import mediapipe as mp
import numpy as np
from typing import List, Tuple, Optional


class LandmarkExtractor:
    """Extract hand landmarks using MediaPipe"""
    
    def __init__(self, 
                 static_image_mode=False,
                 max_num_hands=2,
                 min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        """
        Initialize MediaPipe hands solution
        
        Args:
            static_image_mode: If True, treat input as static images
            max_num_hands: Maximum number of hands to detect
            min_detection_confidence: Minimum confidence for detection
            min_tracking_confidence: Minimum confidence for tracking
        """
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        self.mp_drawing = mp.solutions.drawing_utils
        
    def extract_landmarks(self, image: np.ndarray) -> Optional[np.ndarray]:
        """
        Extract hand landmarks from an image
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            Flattened array of landmarks (21 points * 3 coordinates = 63 features)
            Returns None if no hand detected
        """
        # Convert BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Process the image
        results = self.hands.process(image_rgb)
        
        if results.multi_hand_landmarks:
            # Get landmarks from the first detected hand
            hand_landmarks = results.multi_hand_landmarks[0]
            
            # Extract landmark coordinates
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            
            return np.array(landmarks)
        
        return None
    
    def extract_all_hands_landmarks(self, image: np.ndarray) -> List[np.ndarray]:
        """
        Extract landmarks from all detected hands
        
        Args:
            image: Input image (BGR format)
            
        Returns:
            List of landmark arrays (one per hand)
        """
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        all_landmarks = []
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = []
                for landmark in hand_landmarks.landmark:
                    landmarks.extend([landmark.x, landmark.y, landmark.z])
                all_landmarks.append(np.array(landmarks))
        
        return all_landmarks
    
    def draw_landmarks(self, image: np.ndarray, results) -> np.ndarray:
        """
        Draw landmarks on the image
        
        Args:
            image: Input image
            results: MediaPipe results object
            
        Returns:
            Image with landmarks drawn
        """
        image_copy = image.copy()
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image_copy,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                    self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
                )
        return image_copy
    
    def process_frame(self, frame: np.ndarray) -> Tuple[Optional[np.ndarray], np.ndarray]:
        """
        Process a single frame and extract landmarks
        
        Args:
            frame: Input frame (BGR format)
            
        Returns:
            Tuple of (landmarks array or None, frame with landmarks drawn)
        """
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(image_rgb)
        
        landmarks = None
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            landmarks = np.array(landmarks)
        
        # Draw landmarks on frame
        annotated_frame = self.draw_landmarks(frame, results)
        
        return landmarks, annotated_frame
    
    def __del__(self):
        """Clean up resources"""
        if hasattr(self, 'hands'):
            self.hands.close()

