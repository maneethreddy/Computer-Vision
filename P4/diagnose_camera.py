"""
Diagnostic script to check camera and frame display issues
Run this to see what's happening
"""

import cv2
import sys

print("=" * 60)
print("CAMERA DIAGNOSTIC TOOL")
print("=" * 60)

# Step 1: Test camera initialization
print("\n1. Testing camera initialization...")
if sys.platform == 'win32':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ ERROR: Cannot open camera!")
    print("   - Check if camera is connected")
    print("   - Check Windows camera permissions")
    print("   - Close other apps using the camera")
    sys.exit(1)

print("✓ Camera opened successfully")

# Step 2: Test frame reading
print("\n2. Testing frame reading...")
ret, frame = cap.read()

if not ret:
    print("❌ ERROR: Cannot read frames from camera!")
    print("   - Camera is open but not providing frames")
    print("   - This is a permissions or driver issue")
    sys.exit(1)

if frame is None:
    print("❌ ERROR: Frame is None!")
    sys.exit(1)

print(f"✓ Frame read successfully")
print(f"   - Frame shape: {frame.shape}")
print(f"   - Frame size: {frame.size} bytes")
print(f"   - Frame dtype: {frame.dtype}")

# Step 3: Test frame display
print("\n3. Testing frame display...")
try:
    # Resize for display
    display_frame = cv2.resize(frame, (640, 480))
    
    # Add text
    cv2.putText(display_frame, "Camera Working!", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    print("✓ Frame processed successfully")
    print("\nDisplaying frame for 5 seconds...")
    print("(If you see a window with your camera, it's working!)")
    
    # Show for 5 seconds
    import time
    start_time = time.time()
    while time.time() - start_time < 5:
        cv2.imshow('Camera Test - Press Q to quit', display_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()
    print("✓ Frame display test completed")
    
except Exception as e:
    print(f"❌ ERROR displaying frame: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 4: Test continuous reading
print("\n4. Testing continuous frame reading (10 frames)...")
success_count = 0
for i in range(10):
    ret, frame = cap.read()
    if ret and frame is not None:
        success_count += 1
        print(f"   Frame {i+1}: ✓")
    else:
        print(f"   Frame {i+1}: ❌ Failed")

print(f"\n✓ Successfully read {success_count}/10 frames")

# Step 5: Test with OpenCV window (like the app uses)
print("\n5. Final test - Live camera feed (5 seconds)...")
print("   You should see a window with live camera feed")
print("   Press 'q' to quit or wait 5 seconds")

start_time = time.time()
while True:
    ret, frame = cap.read()
    if ret and frame is not None:
        frame = cv2.flip(frame, 1)  # Mirror effect
        frame = cv2.resize(frame, (640, 480))
        
        # Draw ROI like the app does
        h, w = frame.shape[:2]
        top, bottom = int(h * 0.1), int(h * 0.9)
        left, right = int(w * 0.1), int(w * 0.9)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, "Place hand here", (left, top - 10),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow('Camera Test - Like App', frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        if time.time() - start_time >= 5:
            break
    else:
        print("❌ Failed to read frame during continuous test")
        break

cv2.destroyAllWindows()
cap.release()

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
print("\nPlease copy and paste ALL output from above")
print("Send it to me so I can see what's happening!")




