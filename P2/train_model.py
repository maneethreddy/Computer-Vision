import cv2
import os
import numpy as np
import pickle

class FaceTrainer:
    def __init__(self, dataset_path="dataset", model_path="trained_model"):
        self.dataset_path = dataset_path
        self.model_path = model_path
        
        # Create model directory
        os.makedirs(self.model_path, exist_ok=True)
        
        # Initialize LBPH Face Recognizer with optimized parameters
        # Parameters: radius=1, neighbors=8, grid_x=8, grid_y=8, threshold=80
        # Lower threshold = more strict recognition
        try:
            self.recognizer = cv2.face.LBPHFaceRecognizer_create(
                radius=1,        # LBP radius
                neighbors=8,      # Number of neighbors
                grid_x=8,         # Grid X divisions
                grid_y=8,         # Grid Y divisions
                threshold=80.0    # Recognition threshold (lower = stricter)
            )
            self.use_lbph = True
        except:
            print("Warning: OpenCV contrib face module not found.")
            print("Please install: pip install opencv-contrib-python")
            self.use_lbph = False
    
    def preprocess_image(self, image):
        """Preprocess image for better recognition"""
        # Apply histogram equalization for better contrast
        equalized = cv2.equalizeHist(image)
        
        # Apply slight Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(equalized, (3, 3), 0)
        
        # Ensure consistent size (200x200)
        if image.shape != (200, 200):
            blurred = cv2.resize(blurred, (200, 200))
        
        return blurred
    
    def get_images_and_labels(self):
        """Load images and labels from dataset"""
        faces = []
        labels = []
        label_to_name = {}
        current_label = 0
        
        if not os.path.exists(self.dataset_path):
            print(f"Dataset directory '{self.dataset_path}' not found!")
            return None, None, None
        
        # Iterate through each person's folder
        for person_name in sorted(os.listdir(self.dataset_path)):
            person_path = os.path.join(self.dataset_path, person_name)
            
            if not os.path.isdir(person_path):
                continue
            
            label_to_name[current_label] = person_name
            
            # Load all images for this person
            image_count = 0
            for image_name in sorted(os.listdir(person_path)):
                if image_name.endswith(('.jpg', '.jpeg', '.png')):
                    image_path = os.path.join(person_path, image_name)
                    
                    # Read image in grayscale
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                    
                    if image is not None:
                        # Preprocess image
                        processed = self.preprocess_image(image)
                        faces.append(processed)
                        labels.append(current_label)
                        image_count += 1
            
            print(f"  Loaded {image_count} images for {person_name}")
            current_label += 1
        
        return faces, labels, label_to_name
    
    def train(self):
        """Train the face recognition model"""
        print("Loading images from dataset...")
        faces, labels, label_to_name = self.get_images_and_labels()
        
        if faces is None or len(faces) == 0:
            print("ERROR: No images found in dataset!")
            print("Please register faces first using face_registration.py")
            return False
        
        print(f"Found {len(faces)} images from {len(label_to_name)} person(s)")
        
        if not self.use_lbph:
            print("ERROR: LBPH recognizer not available!")
            return False
        
        print("Training face recognition model...")
        try:
            # Train the recognizer
            labels_array = np.array(labels)
            self.recognizer.train(faces, labels_array)
            
            # Save the trained model
            model_file = os.path.join(self.model_path, "lbph_model.yml")
            self.recognizer.save(model_file)
            print(f"✓ Model saved to {model_file}")
            
            # Save label to name mapping
            mapping_file = os.path.join(self.model_path, "label_to_name.pkl")
            with open(mapping_file, 'wb') as f:
                pickle.dump(label_to_name, f)
            print(f"✓ Label mapping saved to {mapping_file}")
            
            print("\n✓ Training completed successfully!")
            print(f"  - Total images: {len(faces)}")
            print(f"  - Total people: {len(label_to_name)}")
            print(f"  - People registered:")
            for label, name in label_to_name.items():
                count = labels.count(label)
                print(f"    • {name}: {count} images")
            
            return True
            
        except Exception as e:
            print(f"ERROR during training: {e}")
            return False

if __name__ == "__main__":
    trainer = FaceTrainer()
    
    print("=" * 50)
    print("FACE RECOGNITION MODEL TRAINING")
    print("=" * 50)
    print()
    
    success = trainer.train()
    
    if success:
        print("\n✓ Model is ready for face recognition!")
    else:
        print("\n✗ Training failed. Please check the error messages above.")

