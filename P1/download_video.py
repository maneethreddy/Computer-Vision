"""
Download YouTube videos for processing
"""
import argparse
import os
import yt_dlp


def download_video(url: str, output_dir: str = "videos", quality: str = "best") -> str:
    """
    Download a YouTube video
    
    Args:
        url: YouTube video URL
        output_dir: Directory to save video
        quality: Video quality (best, worst, or specific format)
        
    Returns:
        Path to downloaded video file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Configure yt-dlp options with better compatibility
    ydl_opts = {
        'format': 'best[height<=720]/best',  # Try 720p first, fallback to best
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'extract_flat': False,
        'no_warnings': False,
        'quiet': False,
        'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}},
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"Downloading video from: {url}")
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"Video downloaded successfully: {filename}")
            return filename
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description="Download YouTube videos for sign language detection")
    parser.add_argument("--url", type=str, required=True, help="YouTube video URL")
    parser.add_argument("--output", type=str, default="videos", help="Output directory")
    parser.add_argument("--quality", type=str, default="best", help="Video quality (best/worst)")
    
    args = parser.parse_args()
    
    video_path = download_video(args.url, args.output, args.quality)
    if video_path:
        print(f"\nDownload complete! Video saved to: {video_path}")
    else:
        print("\nDownload failed!")


if __name__ == "__main__":
    main()

