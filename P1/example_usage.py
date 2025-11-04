"""
Example usage script for sign language detection project

This script demonstrates the complete workflow:
1. Download a video
2. Collect training data
3. Train a model
4. Detect sign language
"""
import os
from pathlib import Path


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")


def main():
    print("Sign Language Detection Project - Example Workflow")
    print("\nThis script shows the commands to run the complete workflow.")
    print("You can run each step manually or follow this guide.\n")
    
    # Step 1: Download video
    print_section("Step 1: Download YouTube Video")
    print("Download the tutorial video:")
    print('python download_video.py --url "https://www.youtube.com/watch?v=MJCSjXepaAM"')
    print("\nThis will save the video to the 'videos/' directory.")
    
    # Step 2: Collect data
    print_section("Step 2: Collect Training Data")
    print("Collect sign language data from your webcam:")
    print('python collect_data.py --label "hello" --source camera --num_samples 100')
    print('python collect_data.py --label "thank_you" --source camera --num_samples 100')
    print("\nOr collect from a video file:")
    print('python collect_data.py --label "hello" --source videos/video.mp4 --frame_skip 5')
    print("\nRepeat for each sign you want to recognize.")
    
    # Step 3: Train model
    print_section("Step 3: Train the Model")
    print("Train a machine learning model on your collected data:")
    print('python train_model.py --data_dir data --algorithm random_forest')
    print("\nAvailable algorithms: random_forest, svm, knn")
    print("The trained model will be saved to 'models/sign_language_model.pkl'")
    
    # Step 4: Detect sign language
    print_section("Step 4: Detect Sign Language")
    print("Run real-time detection from webcam:")
    print('python detect_sign_language.py --model models/sign_language_model.pkl --source 0')
    print("\nOr detect from a video file:")
    print('python detect_sign_language.py --model models/sign_language_model.pkl --source videos/video.mp4 --output output.mp4')
    
    print_section("Complete Workflow Summary")
    print("1. Download video: python download_video.py --url <URL>")
    print("2. Collect data: python collect_data.py --label <SIGN_NAME> --source camera")
    print("3. Train model: python train_model.py --data_dir data")
    print("4. Detect signs: python detect_sign_language.py --model models/sign_language_model.pkl --source 0")
    print("\nMake sure to install dependencies first:")
    print("pip install -r requirements.txt")


if __name__ == "__main__":
    main()

