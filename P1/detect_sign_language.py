"""
Real-time sign language detection using trained model
"""
import argparse
import cv2
import numpy as np
import pickle
from pathlib import Path

from utils.landmark_extractor import LandmarkExtractor
from utils.video_processor import VideoProcessor


class SignLanguageDetector:
    """Detect sign language in real-time"""
    
    def __init__(self, model_path: str):
        """
        Initialize detector
        
        Args:
            model_path: Path to trained model file
        """
        self.model_path = Path(model_path)
        self.load_model()
        self.landmark_extractor = LandmarkExtractor()
        self.video_processor = VideoProcessor()
    
    def load_model(self):
        """Load trained model from file"""
        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        
        with open(self.model_path, 'rb') as f:
            self.model = pickle.load(f)
        
        print(f"Model loaded from: {self.model_path}")
        print(f"Model type: {type(self.model).__name__}")
    
    def predict(self, landmarks: np.ndarray) -> tuple:
        """
        Predict sign language from landmarks
        
        Args:
            landmarks: Hand landmark array
            
        Returns:
            Tuple of (predicted_label, confidence/probability)
        """
        if landmarks is None:
            return None, 0.0
        
        # Reshape for prediction
        landmarks = landmarks.reshape(1, -1)
        
        # Predict
        prediction = self.model.predict(landmarks)[0]
        
        # Get confidence (probability if available)
        confidence = 0.0
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(landmarks)[0]
            confidence = np.max(proba)
        
        return prediction, confidence
    
    def detect_from_camera(self):
        """Detect sign language from webcam"""
        print("\nStarting real-time sign language detection")
        print("Press 'q' to quit")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Extract landmarks and draw them
                landmarks, annotated_frame = self.landmark_extractor.process_frame(frame)
                
                # Predict sign language
                if landmarks is not None:
                    prediction, confidence = self.predict(landmarks)
                    
                    # Display prediction
                    text = f"Sign: {prediction} ({confidence:.2f})"
                    cv2.putText(annotated_frame, text, (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                else:
                    cv2.putText(annotated_frame, "No hand detected", (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                cv2.imshow("Sign Language Detection", annotated_frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
    
    def detect_from_video(self, video_path: str, output_path: str = None):
        """
        Detect sign language from video file
        
        Args:
            video_path: Path to input video
            output_path: Path to save output video (optional)
        """
        print(f"\nProcessing video: {video_path}")
        
        cap = self.video_processor.load_video(video_path)
        if not cap:
            return
        
        # Get video info
        info = self.video_processor.get_video_info(cap)
        print(f"Video info: {info['width']}x{info['height']} @ {info['fps']} fps")
        
        # Create video writer if output path specified
        writer = None
        if output_path:
            writer = self.video_processor.create_video_writer(
                output_path, info['fps'], info['width'], info['height']
            )
        
        frame_count = 0
        
        try:
            for frame_num, frame in self.video_processor.read_frames(cap):
                # Extract landmarks and draw them
                landmarks, annotated_frame = self.landmark_extractor.process_frame(frame)
                
                # Predict sign language
                if landmarks is not None:
                    prediction, confidence = self.predict(landmarks)
                    
                    text = f"Sign: {prediction} ({confidence:.2f})"
                    cv2.putText(annotated_frame, text, (10, 30),
                               cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Write frame if output specified
                if writer:
                    writer.write(annotated_frame)
                
                frame_count += 1
                if frame_count % 30 == 0:
                    print(f"Processed {frame_count} frames...")
                
                # Display frame (optional, for preview)
                cv2.imshow("Sign Language Detection", annotated_frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        
        finally:
            cap.release()
            if writer:
                writer.release()
            cv2.destroyAllWindows()
        
        print(f"\nFinished processing {frame_count} frames")
        if output_path:
            print(f"Output video saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Detect sign language in real-time or from video")
    parser.add_argument("--model", type=str, required=True,
                       help="Path to trained model file")
    parser.add_argument("--source", type=str, default="0",
                       help="Video source: '0' for webcam, or path to video file")
    parser.add_argument("--output", type=str, default=None,
                       help="Output video path (for video input)")
    
    args = parser.parse_args()
    
    # Initialize detector
    detector = SignLanguageDetector(args.model)
    
    # Detect from camera or video
    if args.source == "0":
        detector.detect_from_camera()
    else:
        detector.detect_from_video(args.source, args.output)


if __name__ == "__main__":
    main()

