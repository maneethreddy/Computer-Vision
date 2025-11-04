import cv2
import os
import numpy as np

class FaceRegistration:
    def __init__(self, dataset_path="dataset"):
        self.dataset_path = dataset_path
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Create dataset directory if it doesn't exist
        if not os.path.exists(self.dataset_path):
            os.makedirs(self.dataset_path)
    
    def register_face(self, name):
        """Register a new face by capturing multiple images"""
        person_path = os.path.join(self.dataset_path, name)
        
        if os.path.exists(person_path):
            response = input(f"Face dataset for '{name}' already exists. Overwrite? (y/n): ")
            if response.lower() != 'y':
                print("Registration cancelled.")
                return False
        
        # Create directory for this person
        os.makedirs(person_path, exist_ok=True)
        
        # Initialize camera
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        
        print(f"\nRegistering face for: {name}")
        print("Instructions:")
        print("1. Position your face in the center of the frame")
        print("2. Ensure good lighting")
        print("3. Look directly at the camera")
        print("4. Press SPACE to capture images (50 images will be captured)")
        print("5. Press 'q' to quit\n")
        
        count = 0
        total_images = 50
        
        while count < total_images:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = cv2.flip(frame, 1)  # Mirror the frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(100, 100)
            )
            
            # Draw rectangle around face
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Save face image
                face_roi = gray[y:y + h, x:x + w]
                
                # Resize to standard size for training
                face_roi = cv2.resize(face_roi, (200, 200))
                
                # Save image
                img_path = os.path.join(person_path, f"{name}_{count}.jpg")
                cv2.imwrite(img_path, face_roi)
                count += 1
                
                # Visual feedback
                cv2.putText(frame, f"Captured: {count}/{total_images}", 
                           (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 
                           0.7, (0, 255, 0), 2)
            
            # Show progress
            cv2.putText(frame, f"Progress: {count}/{total_images}", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       1, (255, 255, 255), 2)
            cv2.putText(frame, "Press 'q' to quit", 
                       (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (255, 255, 255), 2)
            
            cv2.imshow("Face Registration", frame)
            
            # Auto-capture (every 3 frames) or wait for key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
            # Small delay to avoid capturing too quickly
            if count > 0 and count % 5 == 0:
                cv2.waitKey(300)  # Brief pause every 5 images
        
        cap.release()
        cv2.destroyAllWindows()
        
        if count >= total_images:
            print(f"\n✓ Successfully registered {count} images for {name}")
            return True
        else:
            print(f"\n⚠ Only captured {count} images. Registration incomplete.")
            return False
    
    def list_registered_faces(self):
        """List all registered faces"""
        if not os.path.exists(self.dataset_path):
            return []
        
        registered = [d for d in os.listdir(self.dataset_path) 
                     if os.path.isdir(os.path.join(self.dataset_path, d))]
        return registered

if __name__ == "__main__":
    registrar = FaceRegistration()
    
    print("=" * 50)
    print("FACE REGISTRATION SYSTEM")
    print("=" * 50)
    
    # List existing registrations
    existing = registrar.list_registered_faces()
    if existing:
        print(f"\nCurrently registered faces: {', '.join(existing)}")
    else:
        print("\nNo faces registered yet.")
    
    # Register new face
    name = input("\nEnter name to register (or 'q' to quit): ").strip()
    
    if name.lower() != 'q' and name:
        registrar.register_face(name)
    else:
        print("Registration cancelled.")

