# Quick Start Guide

## Camera Issue Fix

Your camera opens but cannot read frames. This is a Windows permissions issue.

### Quick Fix:

1. **Open Windows Camera App first** - This grants basic camera permissions
   - Press Windows Key, type "Camera", open it
   - Let it load and then close it

2. **Grant permissions to Python:**
   - Press `Windows + I` (Settings)
   - Go to **Privacy & security** → **Camera**
   - Enable **"Let desktop apps access your camera"**

3. **Close ALL apps using camera:**
   - Zoom, Skype, Teams, Discord, etc.
   - Some web browsers might have camera access

4. **Try again:**
   ```bash
   python test_camera.py
   ```

### If Still Not Working:

Try running PowerShell as Administrator:
1. Right-click PowerShell → Run as Administrator
2. Navigate to project: `cd C:\Users\abhin\Downloads\cv1`
3. Run: `python test_camera.py`

### Alternative: Use a Different Camera Backend

Edit `gesture_controller.py` line 42 and `test_camera.py` line 19:

Try different backends:
```python
# Option 1: DirectShow (most compatible on Windows)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Option 2: V4L2 (rarely works on Windows)
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Option 3: Default
cap = cv2.VideoCapture(0)
```

### Test Without Camera (Demo Mode)

I can create a demo mode that uses a test video or generates synthetic hand gestures. Would you like that?



