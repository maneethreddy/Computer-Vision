"""
Hand Gesture Recognition Module
Improved version with better accuracy using multiple detection methods
"""

import cv2
import numpy as np


class GestureDetector:
    def __init__(self):
        self.kernel = np.ones((3, 3), np.uint8)
        self.kernel_large = np.ones((5, 5), np.uint8)
        
        # Gesture smoothing - keep history to reduce flickering
        self.gesture_history = []
        self.history_size = 5
        
        # Improved skin color ranges (multiple ranges for better detection)
        self.skin_ranges_hsv = [
            ([0, 20, 70], [20, 255, 255]),      # Light skin
            ([0, 30, 60], [20, 255, 255]),     # Medium skin
            ([0, 48, 80], [20, 255, 255]),     # Darker skin
        ]
        
        # YCbCr color space ranges (more robust for skin detection)
        self.skin_range_ycbcr = ([0, 135, 85], [255, 180, 135])
        
    def detect_gesture(self, frame):
        """Detect hand gesture from frame using improved color-based segmentation"""
        gesture = "None"
        
        try:
            # Create a rectangular region of interest (ROI)
            h, w = frame.shape[:2]
            top, bottom = int(h * 0.1), int(h * 0.9)
            left, right = int(w * 0.1), int(w * 0.9)
            
            # Draw ROI rectangle
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, "Place hand here", (left, top - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            roi = frame[top:bottom, left:right]
            
            # Use multiple skin detection methods for better accuracy
            mask = self.get_skin_mask_improved(roi)
            
            # Improved morphological operations
            mask = self.clean_mask(mask)
            
            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            if contours:
                # Find the largest contour (assumed to be hand)
                max_contour = max(contours, key=cv2.contourArea)
                
                # Improved area threshold based on ROI size
                min_area = (roi.shape[0] * roi.shape[1]) * 0.05  # 5% of ROI
                
                if cv2.contourArea(max_contour) > min_area:
                    # Draw contour on frame
                    cv2.drawContours(frame[top:bottom, left:right], [max_contour], -1, (0, 255, 255), 2)
                    
                    # Classify gesture with improved algorithm
                    gesture = self.classify_gesture_improved(max_contour, roi.shape)
                    
                    # Smooth gesture to reduce flickering
                    gesture = self.smooth_gesture(gesture)
                    
                    # Display gesture on frame
                    cv2.putText(frame, gesture, (10, 50), 
                               cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
                    
                    # Draw visual feedback
                    self.draw_gesture_feedback(frame[top:bottom, left:right], max_contour)
                    
        except Exception as e:
            print(f"Error in gesture detection: {e}")
        
        return frame, gesture
    
    def get_skin_mask_improved(self, roi):
        """Get skin mask using multiple color spaces and ranges"""
        try:
            # Convert to HSV color space
            hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            
            # Combine multiple HSV ranges
            mask_hsv = np.zeros(hsv.shape[:2], dtype=np.uint8)
            for lower, upper in self.skin_ranges_hsv:
                lower = np.array(lower, dtype=np.uint8)
                upper = np.array(upper, dtype=np.uint8)
                mask_temp = cv2.inRange(hsv, lower, upper)
                mask_hsv = cv2.bitwise_or(mask_hsv, mask_temp)
            
            # Try YCbCr color space (with fallback if it fails)
            mask_ycbcr = np.zeros(hsv.shape[:2], dtype=np.uint8)
            try:
                # Try the correct OpenCV constant name
                ycbcr = cv2.cvtColor(roi, cv2.COLOR_BGR2YCrCb)
                lower_ycbcr = np.array(self.skin_range_ycbcr[0], dtype=np.uint8)
                upper_ycbcr = np.array(self.skin_range_ycbcr[1], dtype=np.uint8)
                mask_ycbcr = cv2.inRange(ycbcr, lower_ycbcr, upper_ycbcr)
            except:
                # If YCbCr fails, just use HSV
                pass
            
            # Combine both methods (or just use HSV if YCbCr failed)
            mask = cv2.bitwise_or(mask_hsv, mask_ycbcr)
            
            return mask
        except Exception as e:
            print(f"Error in skin mask detection: {e}")
            # Fallback to basic HSV detection
            try:
                hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
                lower = np.array([0, 20, 70], dtype=np.uint8)
                upper = np.array([20, 255, 255], dtype=np.uint8)
                return cv2.inRange(hsv, lower, upper)
            except:
                return np.zeros(roi.shape[:2], dtype=np.uint8)
    
    def clean_mask(self, mask):
        """Improved mask cleaning with better morphological operations"""
        # Remove noise
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, self.kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, self.kernel_large, iterations=2)
        
        # Fill holes
        mask = cv2.dilate(mask, self.kernel, iterations=1)
        mask = cv2.erode(mask, self.kernel, iterations=1)
        
        # Gaussian blur for smoother edges
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        _, mask = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
        
        return mask
    
    def classify_gesture_improved(self, contour, shape):
        """Improved gesture classification with multiple methods"""
        try:
            # Method 1: Convexity defects
            finger_count_defects = self.count_fingers_defects(contour)
            
            # Method 2: Fingertip detection
            finger_count_tips = self.count_fingers_tips(contour)
            
            # Method 3: Bounding box analysis
            aspect_ratio, hand_orientation = self.analyze_hand_shape(contour)
            
            # Combine methods with weights
            # Defects method is more reliable, tips method is secondary
            if finger_count_defects is not None:
                finger_count = finger_count_defects
                confidence = 0.8
            elif finger_count_tips is not None:
                finger_count = finger_count_tips
                confidence = 0.6
            else:
                # Fallback to simple analysis
                finger_count = self.estimate_fingers_simple(contour, aspect_ratio)
                confidence = 0.4
            
            # Classify gesture with improved logic
            gesture = self.classify_from_count(finger_count, aspect_ratio, hand_orientation)
            
            return gesture
                
        except Exception as e:
            print(f"Error in gesture classification: {e}")
            return "Unknown"
    
    def count_fingers_defects(self, contour):
        """Count fingers using convexity defects (improved algorithm)"""
        try:
            hull = cv2.convexHull(contour, returnPoints=False)
            
            if len(hull) < 3:
                return None
            
            defects = cv2.convexityDefects(contour, hull)
            
            if defects is None or len(defects) == 0:
                return 0  # No defects = fist or closed hand
            
            finger_count = 0
            
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(contour[s][0])
                end = tuple(contour[e][0])
                far = tuple(contour[f][0])
                
                # Calculate distances
                a = np.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                b = np.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                c = np.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                
                # Calculate angle using cosine rule
                if b * c != 0:
                    angle = np.arccos(np.clip((b**2 + c**2 - a**2) / (2 * b * c), -1.0, 1.0))
                    
                    # Improved threshold: angle less than 90 degrees and distance significant
                    # Also check that defect depth is meaningful
                    if angle <= np.pi / 2 and d > 8000:  # Threshold for defect depth
                        finger_count += 1
            
            # Convexity defects give us (fingers - 2) typically
            # But need to handle edge cases
            if finger_count == 0:
                return 0  # Fist
            else:
                return finger_count + 1  # Adjusted count
            
        except Exception:
            return None
    
    def count_fingers_tips(self, contour):
        """Count fingers by detecting fingertips (convex hull points)"""
        try:
            # Get convex hull points
            hull = cv2.convexHull(contour, returnPoints=True)
            
            if len(hull) < 3:
                return None
            
            # Find the center of the hand
            M = cv2.moments(contour)
            if M["m00"] == 0:
                return None
            
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            
            # Count hull points that are far from center (likely fingertips)
            finger_tips = 0
            hull_points = hull.reshape(-1, 2)
            
            # Calculate distances from center
            distances = []
            for point in hull_points:
                dist = np.sqrt((point[0] - cx)**2 + (point[1] - cy)**2)
                distances.append(dist)
            
            if len(distances) == 0:
                return None
            
            # Use 70th percentile as threshold for fingertip detection
            threshold = np.percentile(distances, 70)
            
            for dist in distances:
                if dist > threshold:
                    finger_tips += 1
            
            # Adjust: fingertips usually = fingers + 2 (includes wrist corners)
            if finger_tips > 2:
                return finger_tips - 2
            elif finger_tips <= 2:
                return 0  # Closed hand
            
        except Exception:
            return None
    
    def analyze_hand_shape(self, contour):
        """Analyze hand shape features"""
        try:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h if h > 0 else 0
            
            # Determine orientation
            if aspect_ratio > 1.3:
                orientation = "horizontal"
            elif aspect_ratio < 0.7:
                orientation = "vertical"
            else:
                orientation = "square"
            
            return aspect_ratio, orientation
        except Exception:
            return 1.0, "square"
    
    def estimate_fingers_simple(self, contour, aspect_ratio):
        """Simple fallback estimation"""
        try:
            # Approximate contour to reduce points
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            # Rough estimate based on approximation points
            if len(approx) < 5:
                return 0  # Fist
            elif len(approx) < 8:
                return 2  # Victory
            elif len(approx) < 12:
                return 3  # Three
            else:
                return 5  # Open palm
        except Exception:
            return 0
    
    def classify_from_count(self, finger_count, aspect_ratio, orientation):
        """Classify gesture from finger count with improved logic"""
        # Clamp finger count to valid range
        finger_count = max(0, min(5, int(finger_count)))
        
        if finger_count == 0:
            return "Fist"
        elif finger_count == 1:
            # Could be pointing or thumb
            if aspect_ratio > 1.2:
                return "Fist"  # Likely horizontal fist
            else:
                return "Fist"  # Single finger pointing
        elif finger_count == 2:
            return "Victory"
        elif finger_count == 3:
            return "Three"
        elif finger_count == 4:
            return "Four"
        elif finger_count == 5:
            return "Open Palm"
        else:
            return "Unknown"
    
    def draw_gesture_feedback(self, frame, contour):
        """Draw visual feedback for gesture detection"""
        try:
            hull = cv2.convexHull(contour, returnPoints=False)
            if len(hull) > 3:
                defects = cv2.convexityDefects(contour, hull)
                if defects is not None:
                    for i in range(min(defects.shape[0], 20)):  # Limit to 20 for performance
                        s, e, f, d = defects[i, 0]
                        far = tuple(contour[f][0])
                        # Only draw significant defects
                        if d > 8000:
                            cv2.circle(frame, far, 8, [0, 0, 255], -1)
        except Exception:
            pass
    
    def smooth_gesture(self, gesture):
        """Smooth gesture detection to reduce flickering"""
        self.gesture_history.append(gesture)
        
        # Keep only recent history
        if len(self.gesture_history) > self.history_size:
            self.gesture_history.pop(0)
        
        # Use majority voting from recent history
        if len(self.gesture_history) >= 3:
            # Count occurrences
            gesture_counts = {}
            for g in self.gesture_history:
                gesture_counts[g] = gesture_counts.get(g, 0) + 1
            
            # Get most common gesture
            most_common = max(gesture_counts, key=gesture_counts.get)
            
            # Only use if it appears at least 2 times (reduces noise)
            if gesture_counts[most_common] >= 2:
                return most_common
        
        return gesture
