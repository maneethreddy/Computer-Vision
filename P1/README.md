# Fruit Ninja - Hand Tracking Edition 🍎🍌🍊

A Fruit Ninja-style game controlled by hand gestures using computer vision! Slice falling fruits with your hand movements.

## Features

- **Hand Tracking**: Uses MediaPipe for real-time hand landmark detection
- **Gesture Control**: Slice fruits by moving your hand quickly across the screen
- **Fruit Physics**: Fruits fall from the top with realistic motion
- **Score System**: Earn points by slicing fruits
- **Lives System**: Don't let fruits fall to the bottom!
- **Increasing Difficulty**: Game gets faster as your score increases

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

Or with python3:
```bash
python3 -m pip install -r requirements.txt
```

## Quick Start

### 1. Create Fruit Images (First Time Setup)
The game will auto-generate fruit images if they don't exist, but you can create them manually:
```bash
python3 create_fruit_images.py
```

This creates colorful fruit images in `assets/fruits/`. You can replace these with actual fruit images if you have them!

### 2. Play Fruit Ninja
```bash
python3 fruit_ninja.py
```

Or if you have `python` available:
```bash
python fruit_ninja.py
```

### How to Play

1. **Start the game**: Run `fruit_ninja.py`
2. **Position yourself**: Stand in front of your webcam so your hands are visible
3. **Slice fruits**: Move your hand quickly to slice falling fruits
4. **Score points**: Each fruit gives you 10-15 points
5. **Don't miss**: You lose a life if a fruit reaches the bottom
6. **Game Over**: Game ends when you run out of lives (3 lives total)

### Controls

- **'q'**: Quit the game
- **'r'**: Restart the game

## Project Structure

```
P1/
├── requirements.txt
├── README.md
├── fruit_ninja.py            # Main Fruit Ninja game
├── create_fruit_images.py    # Generate fruit images
├── download_video.py         # Download YouTube videos
├── collect_data.py           # Data collection (for ML projects)
├── train_model.py            # Model training (for ML projects)
├── detect_sign_language.py   # Sign language detection (example)
├── utils/
│   ├── landmark_extractor.py # MediaPipe hand landmark extraction
│   └── video_processor.py    # Video processing utilities
├── data/                     # Data directory
├── models/                   # Models directory
└── videos/                   # Videos directory
```

## Game Mechanics

### Hand Detection
- Uses MediaPipe to track hand landmarks in real-time
- Tracks index finger tip position for slicing detection
- Draws hand landmarks and connections on screen

### Slice Detection
- Detects fast hand movements (minimum speed threshold)
- Checks if slice path intersects any fruits
- Visual feedback with slice trails

### Fruits
- Multiple fruit types with actual images (apple, banana, orange, watermelon, pineapple)
- Random spawn positions and speeds
- Physics-based falling motion
- Rotation animation with spinning fruits
- Fruit images with alpha channel support for smooth blending

## Technical Details

### Hand Tracking
The game uses MediaPipe's Hand Landmarks solution which provides 21 3D hand landmarks. The index finger tip (landmark 8) is used to track hand position for slicing.

### Slice Detection Algorithm
- Calculates hand movement speed between frames
- If speed exceeds threshold, registers as a slice
- Uses line-circle intersection to detect if slice hits any fruits

### Game Loop
1. Capture frame from webcam
2. Extract hand landmarks
3. Detect slicing gestures
4. Update fruit positions
5. Check for collisions
6. Render game graphics
7. Update score and lives

## Requirements

- Python 3.7+
- Webcam
- OpenCV
- MediaPipe
- NumPy

## Tips for Best Gameplay

1. **Lighting**: Make sure you have good lighting so the camera can detect your hands clearly
2. **Background**: Use a plain background (contrasting with your skin tone) for better detection
3. **Hand Position**: Keep your hand visible and well-lit
4. **Quick Movements**: Move your hand quickly to trigger slice detection
5. **Multiple Hands**: The game can detect up to 2 hands simultaneously

## Future Enhancements

- Power-ups and special fruits
- Multiplayer mode
- Different game modes (survival, time attack)
- Sound effects and background music
- High score tracking
- Particle effects when fruits are sliced

## License

Educational project for computer vision and game development learning.

