"""
Collect and label sign language data for training
"""
import argparse
import cv2
import numpy as np
import os
import pandas as pd
from pathlib import Path
import time

from utils.landmark_extractor import LandmarkExtractor
from utils.video_processor import VideoProcessor


class DataCollector:
    """Collect sign language gesture data with labels"""
    
    def __init__(self, output_dir: str = "data"):
        """
        Initialize data collector
        
        Args:
            output_dir: Directory to save collected data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        self.landmark_extractor = LandmarkExtractor()
        self.video_processor = VideoProcessor()
        
        self.collected_data = []
        self.current_label = None
        
    def collect_from_camera(self, label: str, num_samples: int = 100, 
                           sample_delay: float = 0.1):
        """
        Collect data from webcam
        
        Args:
            label: Label for the sign (e.g., "hello", "thank_you")
            num_samples: Number of samples to collect
            sample_delay: Delay between samples in seconds
        """
        print(f"\nCollecting data for label: '{label}'")
        print(f"Press SPACE to start collecting, 'q' to quit")
        
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            return
        
        collecting = False
        sample_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Flip frame horizontally for mirror effect
                frame = cv2.flip(frame, 1)
                
                # Extract landmarks
                landmarks, annotated_frame = self.landmark_extractor.process_frame(frame)
                
                # Display instructions
                cv2.putText(annotated_frame, f"Label: {label}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                if not collecting:
                    cv2.putText(annotated_frame, "Press SPACE to start collecting", 
                               (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
                else:
                    cv2.putText(annotated_frame, f"Collecting... {sample_count}/{num_samples}", 
                               (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                
                cv2.putText(annotated_frame, "Press 'q' to quit", 
                           (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                
                cv2.imshow("Data Collection", annotated_frame)
                
                key = cv2.waitKey(1) & 0xFF
                
                if key == ord('q'):
                    break
                elif key == ord(' ') and not collecting:
                    collecting = True
                    print(f"Started collecting...")
                
                if collecting and landmarks is not None:
                    # Add landmark data with label
                    data_point = {
                        'label': label,
                        'landmarks': landmarks.tolist()
                    }
                    self.collected_data.append(data_point)
                    sample_count += 1
                    
                    print(f"Collected sample {sample_count}/{num_samples}")
                    
                    if sample_count >= num_samples:
                        collecting = False
                        print(f"Finished collecting {num_samples} samples for '{label}'")
                        print("Press SPACE to collect more, or 'q' to save and quit")
                
                time.sleep(sample_delay if collecting else 0.01)
        
        finally:
            cap.release()
            cv2.destroyAllWindows()
    
    def collect_from_video(self, video_path: str, label: str, 
                          frame_skip: int = 5):
        """
        Collect data from a video file
        
        Args:
            video_path: Path to video file
            label: Label for the sign
            frame_skip: Collect every Nth frame
        """
        print(f"\nCollecting data from video: {video_path}")
        print(f"Label: '{label}'")
        
        cap = self.video_processor.load_video(video_path)
        if not cap:
            return
        
        frame_count = 0
        collected_count = 0
        
        try:
            for frame_num, frame in self.video_processor.read_frames(cap):
                if frame_num % frame_skip == 0:
                    landmarks = self.landmark_extractor.extract_landmarks(frame)
                    
                    if landmarks is not None:
                        data_point = {
                            'label': label,
                            'landmarks': landmarks.tolist()
                        }
                        self.collected_data.append(data_point)
                        collected_count += 1
                        
                        if collected_count % 10 == 0:
                            print(f"Collected {collected_count} samples...")
                
                frame_count += 1
        
        finally:
            cap.release()
        
        print(f"Finished collecting {collected_count} samples from video")
    
    def save_data(self, filename: str = "sign_language_data.csv"):
        """
        Save collected data to CSV file
        
        Args:
            filename: Output CSV filename
        """
        if not self.collected_data:
            print("No data collected to save")
            return
        
        # Convert to DataFrame
        df_data = []
        for item in self.collected_data:
            row = {'label': item['label']}
            for i, val in enumerate(item['landmarks']):
                row[f'landmark_{i}'] = val
            df_data.append(row)
        
        df = pd.DataFrame(df_data)
        
        # Save to CSV
        output_path = self.output_dir / filename
        df.to_csv(output_path, index=False)
        print(f"\nData saved to: {output_path}")
        print(f"Total samples: {len(self.collected_data)}")
        print(f"Labels: {df['label'].unique().tolist()}")


def main():
    parser = argparse.ArgumentParser(description="Collect sign language training data")
    parser.add_argument("--output_dir", type=str, default="data", 
                       help="Output directory for data")
    parser.add_argument("--label", type=str, required=True,
                       help="Label for the sign (e.g., 'hello', 'thank_you')")
    parser.add_argument("--source", type=str, default="camera",
                       help="Data source: 'camera' or path to video file")
    parser.add_argument("--num_samples", type=int, default=100,
                       help="Number of samples to collect (for camera)")
    parser.add_argument("--frame_skip", type=int, default=5,
                       help="Collect every Nth frame (for video)")
    
    args = parser.parse_args()
    
    collector = DataCollector(args.output_dir)
    
    if args.source == "camera" or not os.path.exists(args.source):
        collector.collect_from_camera(args.label, args.num_samples)
    else:
        collector.collect_from_video(args.source, args.label, args.frame_skip)
    
    collector.save_data()


if __name__ == "__main__":
    main()

