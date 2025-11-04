#!/usr/bin/env python3
"""
Face Recognition Attendance System - Main Menu
"""

import os
import sys

def print_menu():
    print("\n" + "=" * 60)
    print("  FACE RECOGNITION ATTENDANCE SYSTEM")
    print("=" * 60)
    print("\nMain Menu:")
    print("  1. Register New Face")
    print("  2. Train Recognition Model")
    print("  3. Start Attendance System")
    print("  4. View Attendance Records")
    print("  5. Exit")
    print("=" * 60)

def register_face():
    """Run face registration"""
    print("\n>>> Starting Face Registration...\n")
    os.system("python3 face_registration.py")

def train_model():
    """Train the face recognition model"""
    print("\n>>> Training Face Recognition Model...\n")
    os.system("python3 train_model.py")

def start_attendance():
    """Start the attendance system"""
    print("\n>>> Starting Attendance System...\n")
    os.system("python3 attendance_system.py")

def view_attendance():
    """View attendance records"""
    print("\n>>> Viewing Attendance Records...\n")
    os.system("python3 view_attendance.py")

def main():
    while True:
        print_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            register_face()
        elif choice == '2':
            train_model()
        elif choice == '3':
            # Check if model exists
            if not os.path.exists("trained_model/lbph_model.yml"):
                print("\n⚠ Warning: Model not found!")
                print("Please train the model first (Option 2).")
                response = input("Continue anyway? (y/n): ").strip().lower()
                if response != 'y':
                    continue
            start_attendance()
        elif choice == '4':
            view_attendance()
        elif choice == '5':
            print("\n✓ Thank you for using Face Recognition Attendance System!")
            print("  Goodbye!\n")
            sys.exit(0)
        else:
            print("\n✗ Invalid choice! Please enter 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✓ Program interrupted by user. Goodbye!\n")
        sys.exit(0)

