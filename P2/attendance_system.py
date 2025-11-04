import cv2
import os
import numpy as np
import pickle
import csv
from datetime import datetime
# Pandas only needed for view_attendance.py, not for main system
try:
    import pandas as pd
except ImportError:
    pd = None

class AttendanceSystem:
    def __init__(self, model_path="trained_model", attendance_file="attendance.csv"):
        self.model_path = model_path
        self.attendance_file = attendance_file
        self.recognizer = None
        self.label_to_name = {}
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Track attendance in current session (to prevent duplicates)
        self.session_attendance = set()
        
        # Load trained model
        self.load_model()
        
        # Initialize attendance CSV
        self.init_attendance_csv()
    
    def load_model(self):
        """Load the trained face recognition model"""
        try:
            # Load LBPH model
            model_file = os.path.join(self.model_path, "lbph_model.yml")
            mapping_file = os.path.join(self.model_path, "label_to_name.pkl")
            
            if not os.path.exists(model_file) or not os.path.exists(mapping_file):
                print(f"ERROR: Model files not found in '{self.model_path}'")
                print("Please train the model first using train_model.py")
                return False
            
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read(model_file)
            
            # Load label to name mapping
            with open(mapping_file, 'rb') as f:
                self.label_to_name = pickle.load(f)
            
            print(f"✓ Model loaded successfully!")
            print(f"  - Registered faces: {len(self.label_to_name)}")
            for label, name in self.label_to_name.items():
                print(f"    • {name}")
            return True
            
        except Exception as e:
            print(f"ERROR loading model: {e}")
            return False
    
    def init_attendance_csv(self):
        """Initialize attendance CSV file with headers if it doesn't exist"""
        if not os.path.exists(self.attendance_file):
            with open(self.attendance_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Name', 'Date', 'Time', 'Confidence'])
    
    def mark_attendance(self, name, confidence):
        """Mark attendance for a recognized face"""
        # Create session key (name + date)
        today = datetime.now().strftime("%Y-%m-%d")
        session_key = f"{name}_{today}"
        
        # Check if already marked in this session
        if session_key in self.session_attendance:
            return False
        
        # Mark attendance
        timestamp = datetime.now()
        date = timestamp.strftime("%Y-%m-%d")
        time = timestamp.strftime("%H:%M:%S")
        
        # Write to CSV
        with open(self.attendance_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([name, date, time, f"{confidence:.2f}%"])
        
        # Add to session tracking
        self.session_attendance.add(session_key)
        
        return True
    
    def preprocess_face(self, face_roi):
        """Preprocess face image same as training"""
        # Resize to match training size
        face_resized = cv2.resize(face_roi, (200, 200))
        
        # Apply histogram equalization for better contrast
        equalized = cv2.equalizeHist(face_resized)
        
        # Apply slight Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(equalized, (3, 3), 0)
        
        return blurred
    
    def recognize_face(self, face_roi):
        """Recognize a face from ROI"""
        if self.recognizer is None:
            return None, 0
        
        # Preprocess face same as training
        face_processed = self.preprocess_face(face_roi)
        
        # Predict
        try:
            label, confidence = self.recognizer.predict(face_processed)
            
            # Convert confidence to percentage
            # LBPH returns lower values for better matches
            confidence_percent = max(0, 100 - confidence)
            
            # Adjusted threshold: only recognize if confidence > 40%
            # Lower threshold due to better preprocessing
            if confidence_percent > 40:
                name = self.label_to_name.get(label, "Unknown")
                return name, confidence_percent
            else:
                return "Unknown", confidence_percent
                
        except Exception as e:
            print(f"Recognition error: {e}")
            return None, 0
    
    def run(self):
        """Run the real-time attendance system"""
        if self.recognizer is None:
            print("Cannot run attendance system: Model not loaded!")
            return
        
        # Try to open camera
        cap = cv2.VideoCapture(0)
        
        # Check if camera opened successfully
        if not cap.isOpened():
            print("ERROR: Could not open camera!")
            print("\nTroubleshooting:")
            print("  1. Check if camera is connected")
            print("  2. Make sure no other application is using the camera")
            print("  3. Try disconnecting and reconnecting the camera")
            print("  4. Check camera permissions in system settings")
            cap.release()
            return
        
        # Test if we can read from camera
        ret, test_frame = cap.read()
        if not ret:
            print("ERROR: Could not read from camera!")
            print("Please check camera connection and permissions.")
            cap.release()
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        
        print("\n" + "=" * 50)
        print("FACE RECOGNITION ATTENDANCE SYSTEM")
        print("=" * 50)
        print("\nInstructions:")
        print("  - System will automatically detect and recognize faces")
        print("  - Attendance is marked once per person per day")
        print("  - Press 'q' to quit")
        print("  - Press 'r' to reset today's attendance")
        print("\nStarting camera...\n")
        
        frame_count = 0
        detection_interval = 5  # Process every 5th frame for better performance
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)  # Mirror the frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces (every frame)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )
            
            # Process recognition (every Nth frame for performance)
            frame_count += 1
            if frame_count % detection_interval == 0:
                for (x, y, w, h) in faces:
                    face_roi = gray[y:y + h, x:x + w]
                    name, confidence = self.recognize_face(face_roi)
                    
                    # Draw rectangle and label
                    if name and name != "Unknown":
                        color = (0, 255, 0)  # Green for recognized
                        label_text = f"{name} ({confidence:.1f}%)"
                        
                        # Mark attendance if not already marked
                        if self.mark_attendance(name, confidence):
                            # Show notification
                            cv2.putText(frame, "ATTENDANCE MARKED!", 
                                       (x, y - 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                       0.7, (0, 255, 255), 2)
                    else:
                        color = (0, 0, 255)  # Red for unknown
                        label_text = "Unknown"
                    
                    # Draw bounding box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    
                    # Draw name label
                    cv2.putText(frame, label_text, 
                               (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                               0.7, color, 2)
            
            # Display session info
            today_count = len([k for k in self.session_attendance 
                              if datetime.now().strftime("%Y-%m-%d") in k])
            info_text = f"Today's Attendance: {today_count} | Registered: {len(self.label_to_name)}"
            cv2.putText(frame, info_text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit | 'r' to reset", (10, 60), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 2)
            
            cv2.imshow("Face Recognition Attendance System", frame)
            
            # Keyboard controls
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('r'):
                # Reset today's attendance
                today = datetime.now().strftime("%Y-%m-%d")
                self.session_attendance = {k for k in self.session_attendance 
                                          if today not in k}
                print(f"\n✓ Reset attendance for {datetime.now().strftime('%Y-%m-%d')}")
        
        cap.release()
        cv2.destroyAllWindows()
        
        # Show final statistics
        print("\n" + "=" * 50)
        print("SESSION SUMMARY")
        print("=" * 50)
        print(f"Total attendance marked today: {len(self.session_attendance)}")
        print(f"Attendance saved to: {self.attendance_file}")
        print("\n✓ Attendance system closed.")

if __name__ == "__main__":
    system = AttendanceSystem()
    system.run()

