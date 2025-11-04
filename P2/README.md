# Face Recognition Attendance System

A real-time face recognition system that automatically marks attendance using webcam feed. The system detects and identifies registered faces, logs attendance with timestamps, and prevents duplicate entries.

## Features

✅ **Real-time Face Detection** - Detects multiple faces in live video feed  
✅ **Face Recognition** - Identifies registered individuals using LBPH algorithm  
✅ **Automatic Attendance Marking** - Marks attendance with name, date, and time  
✅ **Confidence Score** - Shows recognition accuracy percentage  
✅ **Duplicate Prevention** - Prevents marking the same person twice in one day  
✅ **CSV Export** - Saves attendance logs in CSV format  
✅ **Excel Export** - Optional export to Excel for analysis  
✅ **Session Tracking** - Tracks attendance per day automatically  

## Project Structure

```
P2/
├── face_registration.py      # Register new faces (capture images)
├── train_model.py            # Train the recognition model
├── attendance_system.py      # Main attendance system
├── view_attendance.py        # View and analyze attendance records
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── dataset/                  # Face images (auto-created)
├── trained_model/            # Trained model files (auto-created)
└── attendance.csv            # Attendance log (auto-created)
```

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Important:** Make sure you have `opencv-contrib-python` installed (not just `opencv-python`) as it includes the face recognition module:
```bash
pip install opencv-contrib-python
```

## Usage

### Step 1: Register Faces

Register individuals by capturing their face images:

```bash
python face_registration.py
```

- Enter the name of the person
- Position face in front of camera
- System will automatically capture 50 images
- Images are saved in `dataset/[name]/` directory

**Instructions:**
- Ensure good lighting
- Look directly at the camera
- Keep face centered in frame
- Wait for automatic capture

### Step 2: Train the Model

Train the face recognition model using registered faces:

```bash
python train_model.py
```

- Loads all images from `dataset/` directory
- Trains LBPH (Local Binary Patterns Histograms) model
- Saves model to `trained_model/` directory

**Output:**
- `lbph_model.yml` - Trained model
- `label_to_name.pkl` - Name mapping

### Step 3: Run Attendance System

Start the real-time attendance system:

```bash
python attendance_system.py
```

**Features:**
- Real-time face detection and recognition
- Automatic attendance marking
- Green bounding box for recognized faces
- Red bounding box for unknown faces
- Shows confidence percentage
- Prevents duplicate attendance per day

**Controls:**
- `q` - Quit application
- `r` - Reset today's attendance (for testing)

### Step 4: View Attendance

View attendance records:

```bash
python view_attendance.py
```

- Displays all attendance records
- Shows statistics by date and person
- Today's attendance summary
- Optional Excel export

## How It Works

### 1. Face Registration
- Uses Haar Cascade for face detection
- Captures 50 images per person
- Saves images in grayscale (200x200 pixels)

### 2. Model Training
- Uses LBPH (Local Binary Patterns Histograms) algorithm
- Trains on registered face images
- Creates unique label for each person

### 3. Face Recognition
- Detects faces in real-time using Haar Cascade
- Recognizes faces using trained LBPH model
- Calculates confidence score (accuracy %)
- Only recognizes if confidence > 50%

### 4. Attendance Logging
- Marks attendance automatically on first recognition
- Logs: Name, Date, Time, Confidence
- Prevents duplicates using session tracking
- Saves to CSV file

## Configuration

### Adjust Recognition Threshold
Edit `attendance_system.py`, line ~58:
```python
if confidence_percent > 50:  # Change threshold here
```

### Adjust Face Detection Sensitivity
Edit `attendance_system.py`, line ~95:
```python
faces = self.face_cascade.detectMultiScale(
    gray,
    scaleFactor=1.1,      # Adjust sensitivity
    minNeighbors=5,       # Higher = more strict
    minSize=(100, 100)    # Minimum face size
)
```

### Change Number of Training Images
Edit `face_registration.py`, line ~30:
```python
total_images = 50  # Change this value
```

## Troubleshooting

### "Model files not found"
- Run `train_model.py` first to create the model

### "No images found in dataset"
- Run `face_registration.py` to register faces first

### "OpenCV contrib module not found"
- Install: `pip install opencv-contrib-python`
- Uninstall regular opencv: `pip uninstall opencv-python`

### Poor Recognition Accuracy
- Ensure good lighting during registration and recognition
- Register multiple angles/expressions
- Increase number of training images
- Adjust detection sensitivity parameters

### Camera Not Working
- Check if camera is connected
- Ensure no other application is using the camera
- Try changing camera index (0, 1, 2) in code

## Output Files

- **`attendance.csv`** - Contains all attendance records
  - Columns: Name, Date, Time, Confidence
- **`dataset/`** - Face images organized by person
- **`trained_model/`** - Model files for recognition

## Success Criteria ✅

- ✅ Detects & recognizes multiple faces in live video
- ✅ Marks attendance automatically without manual input
- ✅ Ignores unknown faces (shows "Unknown")
- ✅ No duplicate attendance in same session/day
- ✅ Shows confidence score for each recognition
- ✅ Saves attendance with date and time
- ✅ Exports to CSV and optional Excel format

## Technical Details

- **Face Detection:** Haar Cascade Classifier
- **Face Recognition:** LBPH (Local Binary Patterns Histograms)
- **Confidence Calculation:** Inverse of LBPH distance (0-100%)
- **Image Processing:** OpenCV
- **Data Storage:** CSV with Pandas
- **Model Format:** YAML (LBPH) + Pickle (mappings)

## License

This project is open source and available for educational purposes.

## Future Enhancements

- Multi-face simultaneous recognition
- Database integration (SQLite/MySQL)
- Attendance reports with graphs
- Email notifications
- Web interface
- Mobile app integration
- Face mask detection
- Temperature integration



# Step 1: Register faces (capture images)
python3 face_registration.py

# Step 2: Train the recognition model
python3 train_model.py

# Step 3: Start the attendance system
python3 attendance_system.py

# Step 4: View attendance records
python3 view_attendance.py