# Hand Gesture Recognition System ✅

## Project Status: COMPLETE

This is a **pure hand gesture recognition system** using Computer Vision. It detects and displays gestures in real-time without any system control features.

## What It Does

✅ **Detects 5 hand gestures**:
- Fist (0-1 fingers)
- Victory (2 fingers)  
- Three (3 fingers)
- Four (4 fingers)
- Open Palm (5 fingers)

✅ **Features**:
- Real-time camera feed
- Live gesture classification
- Visual feedback with contours
- Gesture history tracking
- Modern dark-themed GUI
- No system control - pure recognition only

## How to Use

1. **Run the app**:
   ```bash
   python main.py
   ```

2. **Click the GREEN "START" button**

3. **Show gestures** in front of the camera

4. **Watch** the recognition results appear in real-time!

## Technology Stack

- **OpenCV**: Computer vision and image processing
- **HSV Color Space**: Skin detection
- **Convexity Defects**: Finger counting algorithm
- **Tkinter**: GUI framework
- **NumPy**: Mathematical operations

## Project Files

```
cv1/
├── main.py                 # 🚀 Entry point
├── gesture_controller.py   # 🖥️ GUI & main logic
├── gesture_detector.py     # 👁️ Computer vision
├── gesture_actions.py      # ⚙️ (Optional - not used)
├── requirements.txt        # 📦 Dependencies
├── README.md              # 📖 Full documentation
├── test_camera.py         # 🔧 Camera test
└── [Various .md guides]
```

## Key Features

### Recognition Only
- **No system control**: Detects gestures without performing actions
- **Pure CV project**: Focus on computer vision techniques
- **Real-time display**: Shows what it sees and recognizes
- **Educational**: Great for learning computer vision

### Computer Vision Techniques Used

1. **HSV Color Space**: Better skin detection than RGB
2. **Morphological Operations**: Clean up hand mask
3. **Contour Detection**: Find hand boundaries
4. **Convexity Defects**: Detect spaces between fingers
5. **Geometric Analysis**: Count fingers accurately

## Recognition Pipeline

```
Camera → HSV Conversion → Skin Mask → Morphology → 
Contour Detection → Convex Hull → Convexity Defects → 
Finger Count → Gesture Classification → Display Results
```

## Testing

Test your camera first:
```bash
python test_camera.py
```

Run the recognition system:
```bash
python main.py
```

## Controls

- **▶ Start**: Begin gesture detection
- **⏹ Stop**: Pause detection
- **Camera Feed**: Shows live video with detection overlay
- **Current Gesture**: Displays detected gesture in real-time
- **Gesture History**: Logs recent detections

## Tips for Best Results

✅ **Lighting**: Good, even lighting (avoid harsh shadows)  
✅ **Background**: Plain, contrasting background  
✅ **Position**: Keep hand 30-50cm from camera  
✅ **Stability**: Hold gestures for 2-3 seconds  
✅ **Visibility**: Keep entire hand in green rectangle  

## Customization

### Add More Gestures

Edit `gesture_detector.py` → `classify_gesture()` method

### Adjust Detection

Modify HSV skin color ranges or convexity defect thresholds

### Change GUI

Edit `gesture_controller.py` → `setup_ui()` method

## Optional: Enable Control Features

The `gesture_actions.py` file contains commented-out control code. To enable:

1. Uncomment code in `gesture_controller.py` line 257
2. Add back `from gesture_actions import GestureActions`
3. Enable action execution

But the project works perfectly **as-is** for pure recognition!

## Educational Value

This project demonstrates:
- ✅ Computer vision basics
- ✅ Image processing techniques
- ✅ Real-time video analysis
- ✅ Pattern recognition
- ✅ GUI development
- ✅ Software architecture

## No Errors ✅

All code has been tested and linter-validated. Ready to run!

---

**🎓 Perfect for Computer Vision learning!**




