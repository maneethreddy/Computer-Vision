"""
Video processing utilities
"""
import cv2
import numpy as np
from typing import Optional, Iterator, Tuple


class VideoProcessor:
    """Utilities for video processing"""
    
    @staticmethod
    def load_video(video_path: str) -> Optional[cv2.VideoCapture]:
        """
        Load a video file
        
        Args:
            video_path: Path to video file
            
        Returns:
            VideoCapture object or None if failed
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video {video_path}")
            return None
        return cap
    
    @staticmethod
    def get_video_info(cap: cv2.VideoCapture) -> dict:
        """
        Get video information
        
        Args:
            cap: VideoCapture object
            
        Returns:
            Dictionary with video properties
        """
        return {
            'fps': cap.get(cv2.CAP_PROP_FPS),
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        }
    
    @staticmethod
    def read_frames(cap: cv2.VideoCapture) -> Iterator[Tuple[int, np.ndarray]]:
        """
        Generator to read frames from video
        
        Args:
            cap: VideoCapture object
            
        Yields:
            Tuple of (frame_number, frame)
        """
        frame_num = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            yield frame_num, frame
            frame_num += 1
    
    @staticmethod
    def save_frame(frame: np.ndarray, output_path: str) -> bool:
        """
        Save a frame to disk
        
        Args:
            frame: Frame to save
            output_path: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        return cv2.imwrite(output_path, frame)
    
    @staticmethod
    def extract_frame_at_time(cap: cv2.VideoCapture, time_seconds: float) -> Optional[np.ndarray]:
        """
        Extract a frame at a specific time
        
        Args:
            cap: VideoCapture object
            time_seconds: Time in seconds
            
        Returns:
            Frame at specified time or None
        """
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_number = int(time_seconds * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()
        if ret:
            return frame
        return None
    
    @staticmethod
    def create_video_writer(output_path: str, 
                           fps: float,
                           width: int,
                           height: int,
                           codec: str = 'mp4v') -> Optional[cv2.VideoWriter]:
        """
        Create a video writer
        
        Args:
            output_path: Output video path
            fps: Frames per second
            width: Video width
            height: Video height
            codec: Video codec
            
        Returns:
            VideoWriter object or None if failed
        """
        fourcc = cv2.VideoWriter_fourcc(*codec)
        writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        return writer

