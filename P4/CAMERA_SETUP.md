# Camera Setup Guide for Windows

## Fixing Blank Screen / Camera Not Working

If you see a blank screen when running the gesture recognition app, follow these steps:

### Method 1: Grant Camera Permissions to Python/Application

1. **Open Windows Settings**
   - Press `Windows Key + I`

2. **Go to Privacy Settings**
   - Click on "Privacy & security"
   - Click on "Camera"

3. **Enable Camera Access**
   - Toggle "Camera access" to **ON**
   - Toggle "Let apps access your camera" to **ON**
   - Toggle "Let desktop apps access your camera" to **ON**

### Method 2: Run as Administrator

1. **Open PowerShell or Command Prompt as Administrator**
   - Right-click on PowerShell/CMD
   - Select "Run as Administrator"

2. **Navigate to Project Directory**
   ```bash
   cd C:\Users\abhin\Downloads\cv1
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

### Method 3: Check Camera Availability

Test if your camera works:

```python
import cv2

cap = cv2.VideoCapture(0)
if cap.isOpened():
    print("Camera is available!")
    ret, frame = cap.read()
    if ret:
        print("Camera is working!")
        cv2.imshow('Test', frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Camera opened but cannot read frames")
else:
    print("Camera not detected")
cap.release()
```

### Method 4: Try Different Camera Index

Some systems have multiple cameras. Try changing the camera index in `gesture_controller.py`:

```python
# Line 42 in gesture_controller.py
self.cap = cv2.VideoCapture(0)  # Try 0, 1, 2, etc.
```

### Method 5: Check if Camera is Used by Another App

- Close Skype, Zoom, Teams, or any other apps using the camera
- Restart your browser if webcam access was granted to any website

### Method 6: Windows Camera Privacy Exceptions

If the above doesn't work, add your Python installation to allowed apps:

1. Go to **Settings > Privacy > Camera**
2. Scroll down to "Desktop apps"
3. Find your Python installation and enable it

### Common Issues and Solutions

**Issue**: "Camera opened but cannot read frames"  
**Solution**: Try running the command `python --version` in terminal, then restart the app

**Issue**: Black screen in app but camera works elsewhere  
**Solution**: The issue might be with OpenCV. Try reinstalling:
```bash
pip uninstall opencv-python
pip install opencv-python
```

**Issue**: App crashes immediately  
**Solution**: Check terminal for error messages. Common fix:
```bash
pip install --upgrade opencv-python numpy Pillow pyautogui
```

### Quick Test

Run this test script to verify everything works:

```python
import cv2

print("Testing camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ ERROR: Cannot open camera!")
    print("\nTry these solutions:")
    print("1. Check if another app is using the camera")
    print("2. Grant camera permissions in Windows Settings")
    print("3. Try running as Administrator")
else:
    print("✓ Camera opened successfully!")
    
    ret, frame = cap.read()
    if ret:
        print("✓ Camera is reading frames!")
        cv2.imwrite("camera_test.jpg", frame)
        print("✓ Saved test image as 'camera_test.jpg'")
    else:
        print("❌ Camera opened but cannot read frames")

cap.release()
```

### Still Having Issues?

If none of these work:

1. **Check Device Manager**
   - Press `Windows Key + X`
   - Select "Device Manager"
   - Look for "Cameras" or "Imaging devices"
   - If there's a yellow warning, your camera driver needs updating

2. **Update Camera Driver**
   - Right-click on camera in Device Manager
   - Select "Update driver"
   - Choose "Search automatically for drivers"

3. **Test Camera in Windows Camera App**
   - Open the built-in Windows Camera app
   - If it works there, it's a Python/OpenCV issue
   - If it doesn't work, it's a hardware/permission issue



