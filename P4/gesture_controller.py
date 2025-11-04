"""
Hand Gesture Recognition System
Main GUI application
"""

import tkinter as tk
from tkinter import ttk, Canvas, Label, Frame, Button
import cv2
from PIL import Image, ImageTk
import numpy as np
import sys
from gesture_detector import GestureDetector


class GestureControllerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hand Gesture Recognition System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#2b2b2b')
        
        # Initialize gesture detector
        self.detector = GestureDetector()
        
        # Video capture
        self.cap = None
        self.camera_available = False
        self.initialize_camera()
        
        # UI state
        self.is_running = False
        self.current_gesture = "None"
        self.gesture_history = []
        
        # Setup UI
        self.setup_ui()
    
    def initialize_camera(self):
        """Initialize camera with error handling"""
        try:
            # Try DirectShow backend on Windows for better compatibility
            if sys.platform == 'win32':
                self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            else:
                self.cap = cv2.VideoCapture(0)
            if self.cap.isOpened():
                self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                # Test if camera works
                ret, frame = self.cap.read()
                if ret:
                    self.camera_available = True
                    print("Camera initialized successfully")
                else:
                    self.camera_available = False
                    print("Camera opened but cannot read frames")
            else:
                self.camera_available = False
                print("Failed to open camera. Please check permissions and camera availability")
        except Exception as e:
            self.camera_available = False
            print(f"Error initializing camera: {e}")
        
    def setup_ui(self):
        """Create and arrange UI components"""
        
        # Header
        header = Frame(self.root, bg='#1e1e1e', height=80)
        header.pack(fill='x', pady=(0, 10))
        
        title_label = Label(header, text="👋 Hand Gesture Control System", 
                           font=('Helvetica', 24, 'bold'), 
                           bg='#1e1e1e', fg='#00ff88')
        title_label.pack(pady=20)
        
        # Main container
        main_container = Frame(self.root, bg='#2b2b2b')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Video feed
        left_panel = Frame(main_container, bg='#2b2b2b')
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        video_frame = Frame(left_panel, bg='#1e1e1e', relief='raised', bd=2)
        video_frame.pack(fill='both', expand=True)
        
        video_label = Label(video_frame, text="📹 Camera Feed", 
                           font=('Helvetica', 14), 
                           bg='#1e1e1e', fg='#ffffff')
        video_label.pack(pady=10)
        
        self.video_canvas = Canvas(video_frame, bg='#000000', width=640, height=480)
        self.video_canvas.pack(padx=10, pady=10)
        
        # Show welcome message
        self.video_canvas.create_text(320, 240, text="Click 'START' to begin gesture detection", 
                                     fill='#00ff88', font=('Helvetica', 20, 'bold'))
        
        # Control buttons
        button_frame = Frame(left_panel, bg='#2b2b2b')
        button_frame.pack(fill='x', pady=10)
        
        self.start_btn = Button(button_frame, text="▶ Start", 
                               font=('Helvetica', 12, 'bold'),
                               bg='#00ff88', fg='#000000',
                               command=self.start_detection,
                               relief='flat', padx=20, pady=10)
        self.start_btn.pack(side='left', padx=5)
        
        self.stop_btn = Button(button_frame, text="⏹ Stop", 
                              font=('Helvetica', 12, 'bold'),
                              bg='#ff4444', fg='#ffffff',
                              command=self.stop_detection,
                              relief='flat', padx=20, pady=10)
        self.stop_btn.pack(side='left', padx=5)
        
        self.stop_btn.config(state='disabled')
        
        # Camera status label
        if not self.camera_available:
            camera_warning = Label(left_panel, 
                                  text="⚠ Camera not available!\nPlease check permissions\nor connect a camera",
                                  font=('Helvetica', 12, 'bold'),
                                  bg='#ff4444', fg='#ffffff',
                                  pady=20)
            camera_warning.pack(fill='both', pady=10)
        
        # Right panel - Info and controls
        right_panel = Frame(main_container, bg='#2b2b2b', width=350)
        right_panel.pack(side='right', fill='y', padx=(10, 0))
        right_panel.pack_propagate(False)
        
        # Current gesture display
        gesture_frame = Frame(right_panel, bg='#1e1e1e', relief='raised', bd=2)
        gesture_frame.pack(fill='x', pady=(0, 10))
        
        Label(gesture_frame, text="Current Gesture", 
             font=('Helvetica', 14, 'bold'),
             bg='#1e1e1e', fg='#00ff88').pack(pady=10)
        
        self.gesture_display = Label(gesture_frame, text="None", 
                                     font=('Helvetica', 32, 'bold'),
                                     bg='#1e1e1e', fg='#00ff88')
        self.gesture_display.pack(pady=20)
        
        # Gesture history
        history_frame = Frame(right_panel, bg='#1e1e1e', relief='raised', bd=2)
        history_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        Label(history_frame, text="Gesture History", 
             font=('Helvetica', 12, 'bold'),
             bg='#1e1e1e', fg='#ffffff').pack(pady=10)
        
        self.history_listbox = tk.Listbox(history_frame, 
                                          font=('Courier', 10),
                                          bg='#2b2b2b', fg='#00ff88',
                                          selectbackground='#00ff88',
                                          selectforeground='#000000')
        self.history_listbox.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Control actions
        controls_frame = Frame(right_panel, bg='#1e1e1e', relief='raised', bd=2)
        controls_frame.pack(fill='x')
        
        Label(controls_frame, text="Recognized Gestures", 
             font=('Helvetica', 12, 'bold'),
             bg='#1e1e1e', fg='#ffffff').pack(pady=10)
        
        controls_text = """
👊 Fist (0-1 fingers)
✌ Victory (2 fingers)  
🤟 Three (3 fingers)
✋ Four (4 fingers)
🖐 Open Palm (5 fingers)

Click START and make gestures
to see them detected!
        """
        
        controls_label = Label(controls_frame, text=controls_text,
                              font=('Courier', 9),
                              bg='#1e1e1e', fg='#cccccc',
                              justify='left')
        controls_label.pack(pady=10, padx=10)
        
        # Status bar
        status_bar = Frame(self.root, bg='#1e1e1e', height=40)
        status_bar.pack(fill='x', side='bottom', pady=(10, 0))
        
        self.status_label = Label(status_bar, text="● Ready", 
                                 font=('Helvetica', 10),
                                 bg='#1e1e1e', fg='#00ff88')
        self.status_label.pack(side='left', padx=20)
        
    def start_detection(self):
        """Start gesture detection"""
        if not self.camera_available:
            self.status_label.config(text="● Camera not available!")
            return
        
        # Clear the welcome message
        self.video_canvas.delete("all")
        
        self.is_running = True
        self.start_btn.config(state='disabled')
        self.stop_btn.config(state='normal')
        self.status_label.config(text="● Running - Show your hand to the camera")
        self.update_frame()
        
    def stop_detection(self):
        """Stop gesture detection"""
        self.is_running = False
        self.start_btn.config(state='normal')
        self.stop_btn.config(state='disabled')
        self.status_label.config(text="● Stopped")
        self.current_gesture = "None"
        self.gesture_display.config(text="None")
        
    def update_frame(self):
        """Update video frame and detect gestures"""
        if self.is_running and self.camera_available:
            try:
                ret, frame = self.cap.read()
                if not ret:
                    # Show error message on canvas
                    self.video_canvas.delete("all")
                    self.video_canvas.create_text(320, 240, text="Camera Error\nCheck if camera is available", 
                                                 fill='#ff4444', font=('Helvetica', 16, 'bold'))
                elif frame is not None and frame.size > 0:
                    try:
                        # Flip frame horizontally for mirror effect
                        frame = cv2.flip(frame, 1)
                        
                        # First draw the ROI rectangle on the frame
                        h, w = frame.shape[:2]
                        top, bottom = int(h * 0.1), int(h * 0.9)
                        left, right = int(w * 0.1), int(w * 0.9)
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                        cv2.putText(frame, "Place hand here", (left, top - 10),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                        
                        # Detect gesture with error handling - but always show frame
                        gesture = "None"
                        try:
                            frame, gesture = self.detector.detect_gesture(frame)
                        except Exception:
                            # Gesture detection failed, continue with frame
                            pass
                        
                        # Update gesture display if changed
                        if gesture != self.current_gesture:
                            self.current_gesture = gesture
                            self.gesture_display.config(text=gesture)
                            
                            # Add to history
                            if gesture != "None":
                                self.gesture_history.append(gesture)
                                self.history_listbox.insert(0, gesture)
                                if len(self.history_listbox.get(0, tk.END)) > 10:
                                    self.history_listbox.delete(10)
                            
                            # Execute gesture action
                            if gesture != "None":
                                self.execute_action(gesture)
                        
                        # Convert to RGB and display - ALWAYS do this
                        try:
                            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                            img = Image.fromarray(frame_rgb)
                            img = img.resize((640, 480))
                            img_tk = ImageTk.PhotoImage(image=img)
                            
                            # Clear canvas and display new frame
                            self.video_canvas.delete("all")
                            self.video_canvas.create_image(320, 240, image=img_tk, anchor='center')
                            self.video_canvas.image = img_tk  # Keep reference - IMPORTANT!
                        except Exception as e:
                            pass
                    except Exception as e:
                        # Show error on canvas
                        self.video_canvas.delete("all")
                        self.video_canvas.create_text(320, 240, text=f"Processing Error:\n{str(e)}", 
                                                     fill='#ff4444', font=('Helvetica', 12, 'bold'))
                else:
                    self.video_canvas.delete("all")
                    self.video_canvas.create_text(320, 240, text="No frame data", 
                                                 fill='#ff4444', font=('Helvetica', 16, 'bold'))
            except Exception as e:
                self.video_canvas.delete("all")
                self.video_canvas.create_text(320, 240, text=f"Camera Error:\n{str(e)}", 
                                             fill='#ff4444', font=('Helvetica', 12, 'bold'))
            
            # Schedule next update (always schedule, even on errors)
            self.root.after(30, self.update_frame)
        else:
            # If not running, don't schedule updates
            pass
    
    def execute_action(self, gesture):
        """Execute action based on gesture"""
        # Option 1: No actions (recognition only)
        self.status_label.config(text=f"● Gesture detected: {gesture}")
        
        # Option 2: Uncomment below to enable system controls
        # try:
        #     if gesture == "Fist":
        #         self.actions.toggle_window()
        #     elif gesture == "Victory":
        #         self.actions.take_screenshot()
        #     elif gesture == "Three":
        #         self.actions.volume_up()
        #     elif gesture == "Four":
        #         self.actions.volume_down()
        #     elif gesture == "Open Palm":
        #         self.actions.click_action()
        #     
        #     self.status_label.config(text=f"● Action executed: {gesture}")
        # except Exception as e:
        #     self.status_label.config(text=f"● Error: {str(e)}")
    
    def run(self):
        """Start the application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Cleanup on window close"""
        self.is_running = False
        if self.cap:
            self.cap.release()
        self.root.destroy()

