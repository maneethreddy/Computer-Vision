"""
Gesture Action Executor
Handles system control actions based on gestures
"""

import pyautogui
import time


class GestureActions:
    def __init__(self):
        self.last_action_time = time.time()
        self.action_delay = 1.0  # Minimum delay between actions (seconds)
        
    def _rate_limit(self):
        """Rate limit actions to prevent spam"""
        current_time = time.time()
        if current_time - self.last_action_time < self.action_delay:
            return False
        self.last_action_time = current_time
        return True
    
    def toggle_window(self):
        """Toggle current window visibility"""
        if not self._rate_limit():
            return
        try:
            # Simulate Alt+Tab for window switching
            pyautogui.hotkey('alt', 'tab')
        except Exception as e:
            print(f"Error in toggle_window: {e}")
    
    def take_screenshot(self):
        """Take a screenshot"""
        if not self._rate_limit():
            return
        try:
            screenshot = pyautogui.screenshot()
            filename = f"screenshot_{int(time.time())}.png"
            screenshot.save(filename)
            print(f"Screenshot saved: {filename}")
        except Exception as e:
            print(f"Error in take_screenshot: {e}")
    
    def volume_up(self):
        """Increase system volume"""
        if not self._rate_limit():
            return
        try:
            pyautogui.press('volumeup')
        except Exception as e:
            print(f"Error in volume_up: {e}")
    
    def volume_down(self):
        """Decrease system volume"""
        if not self._rate_limit():
            return
        try:
            pyautogui.press('volumedown')
        except Exception as e:
            print(f"Error in volume_down: {e}")
    
    def next_item(self):
        """Next item (e.g., next song, next slide)"""
        if not self._rate_limit():
            return
        try:
            pyautogui.press('right')
        except Exception as e:
            print(f"Error in next_item: {e}")
    
    def previous_item(self):
        """Previous item (e.g., previous song, previous slide)"""
        if not self._rate_limit():
            return
        try:
            pyautogui.press('left')
        except Exception as e:
            print(f"Error in previous_item: {e}")
    
    def click_action(self):
        """Perform a click action"""
        if not self._rate_limit():
            return
        try:
            pyautogui.click()
        except Exception as e:
            print(f"Error in click_action: {e}")

