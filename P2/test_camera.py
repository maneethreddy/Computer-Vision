#!/usr/bin/env python3
"""Simple camera test to verify everything works"""

import cv2
import sys

print("Testing camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera not available!")
    sys.exit(1)

print("Camera opened successfully!")
print("Window should appear - showing camera feed for 5 seconds...")
print("Press any key in the window to close early, or wait 5 seconds")

count = 0
while count < 150:  # ~5 seconds at 30fps
    ret, frame = cap.read()
    if not ret:
        print("Failed to read frame")
        break
    
    frame = cv2.flip(frame, 1)
    cv2.putText(frame, "Camera Test - Press any key to close", 
               (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Camera Test", frame)
    
    if cv2.waitKey(1) & 0xFF != 255:
        break
    
    count += 1

cap.release()
cv2.destroyAllWindows()
print("Camera test complete!")


