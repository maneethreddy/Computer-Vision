# How to Use the Hand Gesture App

## Quick Start Guide

### Step 1: Launch the App
```bash
python main.py
```

A window will open with a dark-themed interface.

### Step 2: Click the GREEN "START" Button ⏯️

When you first open the app, the camera area shows:
```
"Click 'START' to begin gesture detection"
```

**This is NORMAL!** The app starts in paused mode.

### Step 3: Camera Feed Appears 📹

After clicking START:
- Green rectangle appears on screen (detection area)
- Your camera feed becomes visible
- Status bar says "Running - Show your hand to the camera"

### Step 4: Make Gestures ✋

Place your hand inside the **green rectangle** on screen.

Try these gestures:

| Gesture | How to Make | Action |
|---------|-------------|--------|
| **Fist** | Close your hand completely (0 fingers up) | 🪟 Toggle Windows |
| **Victory** | ✌️ Two fingers up (index + middle) | 📸 Take Screenshot |
| **Three** | 🤟 Three fingers up | 🔊 Volume Up |
| **Four** | ✋ Four fingers up | 🔉 Volume Down |
| **Open Palm** | 🖐️ All five fingers up | 🖱️ Click |

### Step 5: Watch the Magic ✨

- **Current Gesture**: Shows detected gesture in large green text
- **Gesture History**: Logs your recent gestures
- **Status Bar**: Shows action confirmations

### Step 6: Stop When Done ⏹️

Click the RED "STOP" button to pause detection.

---

## Visual Guide

```
┌─────────────────────────────────────────────────────┐
│  Hand Gesture Recognition & Control System         │
├─────────────────────────────────────────────────────┤
│                                                     │
│  📹 Camera Feed               Current Gesture      │
│  ┌─────────────────┐          ┌──────────────────┐│
│  │                 │          │                  ││
│  │  ╔═════════════╗ │          │      None         ││
│  │  ║             ║ │          └──────────────────┘│
│  │  ║             ║ │                              │
│  │  ║  [GREEN]    ║ │    Gesture History          │
│  │  ║             ║ │    ┌──────────────────┐     │
│  │  ║             ║ │    │                  │     │
│  │  ╚═════════════╝ │    │                  │     │
│  │                 │    └──────────────────┘     │
│  └─────────────────┘                              │
│                                                     │
│  ▶ START  ⏹ STOP                                  │
│                                                     │
│  Control Actions                                   │
│  • Fist → Toggle Window                            │
│  • Victory → Screenshot                            │
│  • Three → Volume Up                               │
│  • Four → Volume Down                              │
│  • Open Palm → Click                               │
│                                                     │
├─────────────────────────────────────────────────────┤
│  ● Ready                                           │
└─────────────────────────────────────────────────────┘
```

---

## Troubleshooting

### Blank Screen?

**This is OK!** Just click the **GREEN START button**.

The app intentionally starts paused.

### Camera Not Working?

Run the camera test:
```bash
python test_camera.py
```

See `CAMERA_SETUP.md` for detailed fixes.

### Gesture Not Detected?

Try these tips:
1. ✅ Good lighting (but not direct sunlight)
2. ✅ Plain background (avoid patterns)
3. ✅ Hold gesture for 2-3 seconds
4. ✅ Keep hand fully inside green rectangle
5. ✅ Stay 30-50cm from camera

### Actions Not Working?

- **Rate limiting**: Actions have 1-second cooldown
- **Permissions**: Some actions need admin rights
- **Check terminal**: Errors print there

---

## Tips for Best Results 🎯

### Lighting
- ✅ Bright, even lighting
- ❌ Avoid direct sunlight
- ❌ Avoid harsh shadows

### Background
- ✅ Plain wall or backdrop
- ❌ Avoid busy patterns
- ❌ Avoid colors matching skin tone

### Hand Position
- ✅ Fully visible in frame
- ✅ Flat against green rectangle
- ✅ Fingers clearly separated
- ❌ Don't overlap fingers

### Gesture Making
- ✅ Hold for 2-3 seconds
- ✅ Make gestures clearly
- ✅ Fingers fully extended/closed
- ❌ Don't rush gestures

---

## Example Usage

1. **Control Music While Working**
   - Make "Three" gesture → Volume up
   - Make "Four" gesture → Volume down

2. **Quick Screenshots**
   - Make "Victory" ✌️ → Instant screenshot!

3. **Navigate Windows**
   - Make "Fist" → Switch between apps
   - Make "Open Palm" → Click something

---

## Advanced

### Customize Gestures

Edit `gesture_detector.py` to change detection logic.

### Add New Actions

Edit `gesture_actions.py` to add more controls.

### Adjust Sensitivity

Edit detection thresholds in `classify_gesture()` function.

---

## Still Need Help?

1. Check terminal for error messages
2. Run `python test_camera.py` to test camera
3. See `CAMERA_SETUP.md` for camera issues
4. See `QUICK_START.md` for quick reference

---

**Remember: Click START! The app waits for you! 🚀**




