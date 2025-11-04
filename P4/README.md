# Hand Gesture Recognition System 👋

A real-time hand gesture recognition system built with Computer Vision, using OpenCV for hand tracking and a modern GUI built with Tkinter.

## Features ✨

- **Real-time Gesture Detection**: Live camera feed with hand contour tracking
- **Multiple Predefined Gestures**: Recognize various hand gestures by finger count
- **Visual Feedback**: See detected contours and gesture classification on screen
- **Modern GUI**: Beautiful dark-themed interface with real-time feedback
- **Gesture History**: Track your recent gestures

## Recognized Gestures 🤏

| Gesture | Fingers | Description |
|---------|---------|-------------|
| **Fist** | 0-1 | Closed hand with no fingers extended |
| **Victory** | 2 | Peace sign with index and middle finger up |
| **Three** | 3 | Three fingers extended |
| **Four** | 4 | Four fingers extended |
| **Open Palm** | 5 | All five fingers fully extended |

## Requirements 📋

- Python 3.7 or higher
- Webcam/Camera
- Windows/Mac/Linux

## Installation 🚀

1. **Clone or download this repository**
   ```bash
   cd cv1
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test your camera (optional but recommended)**
   ```bash
   python test_camera.py
   ```

## Usage 💻

1. **Run the application**
   ```bash
   python main.py
   ```
   
   **Note**: If camera issues occur, the DirectShow backend is used automatically on Windows.

2. **Start gesture detection**
   - **Important**: The camera area shows blank initially - this is normal!
   - Click the "▶ Start" button (GREEN button)
   - Camera feed will appear immediately
   - Position your hand in front of the camera
   - Make one of the recognized gestures

3. **View results**
   - Current gesture is displayed in large text
   - Gesture history shows recent detections
   - Actions are executed automatically

4. **Stop detection**
   - Click the "⏹ Stop" button when done

## Tips for Best Results 🎯

- **Lighting**: Ensure good lighting conditions (but avoid direct sunlight)
- **Background**: Use a plain, contrasting background for better detection
- **Distance**: Keep your hand 30-50cm from the camera
- **Stability**: Hold gestures for 2-3 seconds for reliable detection
- **Clear View**: Make sure your entire hand is visible within the green rectangle
- **Skin Color**: Works best with light to medium skin tones in good lighting

## Project Structure 📁

```
cv1/
├── main.py                 # Application entry point
├── gesture_controller.py   # Main GUI application
├── gesture_detector.py     # MediaPipe hand detection
├── gesture_actions.py      # (Optional) System control actions
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## How It Works 🔧

### Gesture Detection Pipeline

1. **Camera Capture**: Live video feed from webcam
2. **Hand Segmentation**: Color-based skin detection using HSV color space
3. **Contour Detection**: Find hand contour using OpenCV
4. **Feature Extraction**: Convexity defects and geometric features calculated
5. **Gesture Classification**: Rules-based classifier identifies gesture by finger count
6. **Visual Feedback**: Contours and gesture displayed on screen with classification

### Technical Details

- **OpenCV**: Video capture, image processing, and hand segmentation
- **HSV Color Space**: Robust skin color detection for hand tracking
- **Convexity Defects**: Counting fingers using geometric analysis
- **Tkinter**: Cross-platform GUI framework
- **NumPy**: Mathematical operations on image data

## Customization 🎨

### Adding New Gestures

Edit `gesture_detector.py` in the `classify_gesture()` method:

```python
elif total_fingers == X and specific_condition:
    return "Your Gesture Name"
```

### Optional: Adding System Control Actions

If you want to enable system control, uncomment the code in `gesture_controller.py` in the `execute_action()` method.

## Troubleshooting 🔧

### Camera not working
- Check camera permissions
- Ensure no other application is using the camera
- Try changing camera index in `gesture_controller.py`: `self.cap = cv2.VideoCapture(1)`

### Gestures not detected
- Improve lighting conditions
- Move closer to camera
- Keep hand fully visible
- Ensure good contrast with background

### Actions not working
- Check if PyAutoGUI has necessary permissions
- On Mac, grant accessibility permissions in System Preferences
- Action rate limiting prevents duplicate triggers

## Future Enhancements 🚀

- [ ] Machine learning-based gesture classification
- [ ] Custom gesture training
- [ ] Support for multiple hands
- [ ] Voice feedback
- [ ] Gesture recording and playback
- [ ] Integration with home automation
- [ ] Mobile app companion

## License 📄

This project is open source and available for educational purposes.

## Acknowledgments 🙏

- **OpenCV** community for computer vision tools
- **Tkinter** for GUI development
- **PyAutoGUI** for system automation

## Contact 💬

Feel free to modify and enhance this project for your needs!

---

**Made with ❤️ using Computer Vision**

