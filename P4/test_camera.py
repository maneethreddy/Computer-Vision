"""
Quick camera test script
Run this to check if your camera is working properly
"""

import cv2
import sys
import os

# Fix Windows console encoding for Unicode
if sys.platform == 'win32':
    try:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except:
        pass

print("=" * 50)
print("Camera Test Script")
print("=" * 50)

print("\n1. Testing camera initialization...")
# Try DirectShow backend on Windows (more reliable)
if sys.platform == 'win32':
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
else:
    cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ ERROR: Cannot open camera!")
    print("\n📋 Troubleshooting steps:")
    print("   1. Check if another app is using the camera")
    print("   2. Grant camera permissions in Windows Settings")
    print("   3. Try running as Administrator")
    print("   4. See CAMERA_SETUP.md for detailed instructions")
    input("\nPress Enter to exit...")
else:
    print("✓ Camera opened successfully!")
    
    print("\n2. Testing frame capture...")
    ret, frame = cap.read()
    if ret:
        print("✓ Camera is reading frames!")
        print(f"✓ Frame size: {frame.shape}")
        
        print("\n3. Testing video capture (5 seconds)...")
        print("   Showing live feed - press 'q' to quit or wait 5 seconds")
        
        import time
        start_time = time.time()
        while True:
            ret, frame = cap.read()
            if ret:
                # Add text overlay
                cv2.putText(frame, "Camera Test - Press 'q' to quit", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (0, 255, 0), 2)
                
                elapsed = int(time.time() - start_time)
                cv2.putText(frame, f"Time: {elapsed}s", 
                           (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 
                           1, (255, 0, 0), 2)
                
                cv2.imshow('Camera Test', frame)
                
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\n✓ Manual quit - Camera is working!")
                    break
                
                if elapsed >= 5:
                    print("\n✓ 5 seconds elapsed - Camera is working!")
                    break
            else:
                print("❌ Failed to read frame!")
                break
        
        cv2.destroyAllWindows()
        
        print("\n4. Saving test image...")
        ret, frame = cap.read()
        if ret:
            cv2.imwrite("camera_test.jpg", frame)
            print("✓ Saved test image as 'camera_test.jpg'")
        
        print("\n" + "=" * 50)
        print("✅ Camera test PASSED!")
        print("=" * 50)
        print("\nYour camera is working. You can now run main.py")
    else:
        print("❌ Camera opened but cannot read frames")
        print("\nThis usually means:")
        print("   - Another application is using the camera")
        print("   - Camera permissions are restricted")
        print("   - Camera driver issue")

cap.release()
print("\nExiting...")

