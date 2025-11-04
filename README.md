# Computer Vision Projects 🎥

A collection of computer vision projects demonstrating various applications using OpenCV, MediaPipe, and machine learning techniques.

## Projects Overview

### [P1: Fruit Ninja Game](./P1/) 🍎🍌🍊
A Fruit Ninja-style game controlled by hand gestures using computer vision! Slice falling fruits with your hand movements.

**Features:**
- Real-time hand tracking using MediaPipe
- Gesture-controlled gameplay
- Score system and lives tracking
- Increasing difficulty levels

**Tech Stack:** OpenCV, MediaPipe, NumPy

---

### [P2: Face Recognition Attendance System](./P2/) 👤
A real-time face recognition system that automatically marks attendance using webcam feed.

**Features:**
- Real-time face detection and recognition
- Automatic attendance marking with timestamps
- Duplicate prevention
- CSV/Excel export functionality
- Confidence scoring

**Tech Stack:** OpenCV (contrib), LBPH Algorithm, Haar Cascade

---

### [P3: Motion Detection System](./P3/) 🚨
A real-time motion detection system with alarm and notification features.

**Features:**
- Real-time motion detection
- Adjustable sensitivity controls
- Region of Interest (ROI) selection
- Audio alarm system
- Motion event logging

**Tech Stack:** OpenCV, PyQt5, Pygame

---

### [P4: Hand Gesture Recognition System](./P4/) 👋
A real-time hand gesture recognition system with modern GUI for gesture-based control.

**Features:**
- Real-time gesture detection (Fist, Victory, Three, Four, Open Palm)
- Visual feedback with contour tracking
- Modern dark-themed GUI
- Gesture history tracking
- Optional system control actions

**Tech Stack:** OpenCV, MediaPipe, Tkinter

---

### [P5: Number Plate Detection](./P5/) 🚗
An OCR-based number plate detection and recognition system for vehicles.

**Features:**
- Automatic number plate detection
- OCR text extraction using Tesseract
- Indian license plate format recognition
- Image preprocessing and enhancement
- Character correction algorithms

**Tech Stack:** OpenCV, Tesseract OCR, NumPy

---

## Getting Started

Each project is self-contained with its own:
- `requirements.txt` - Python dependencies
- `README.md` - Detailed documentation
- Example code and utilities

### Prerequisites

- Python 3.7 or higher
- Webcam/Camera (for real-time projects)
- pip package manager

### Installation

1. Clone this repository:
```bash
git clone https://github.com/maneethreddy/Computer-Vision.git
cd Computer-Vision
```

2. Navigate to any project directory:
```bash
cd P1  # or P2, P3, P4, P5
```

3. Install project-specific dependencies:
```bash
pip install -r requirements.txt
```

4. Follow the project-specific README for detailed usage instructions.

---

## Project Structure

```
Computer-Vision/
├── P1/          # Fruit Ninja Game
├── P2/          # Face Recognition Attendance System
├── P3/          # Motion Detection System
├── P4/          # Hand Gesture Recognition System
├── P5/          # Number Plate Detection
└── README.md    # This file
```

---

## Common Dependencies

Most projects use:
- **OpenCV** - Computer vision library
- **NumPy** - Numerical computing
- **MediaPipe** - Hand tracking and pose estimation (P1, P4)
- **Tesseract OCR** - Optical character recognition (P5)

---

## License

This project is open source and available for educational purposes.

---

## Author

**Maneeth Reddy**

---

## Contributions

Feel free to fork, modify, and enhance these projects for your needs!

---

## Acknowledgments

- OpenCV community for computer vision tools
- MediaPipe team for hand tracking solutions
- All open-source contributors


