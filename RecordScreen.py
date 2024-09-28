import cv2
import numpy as np
import pyautogui
import keyboard  # For detecting 'q' keypress to stop recording
from pynput import mouse, keyboard as pynput_keyboard
import time
import threading
import json

# Screen resolution
SCREEN_SIZE = tuple(pyautogui.size())

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, SCREEN_SIZE)

# Global variables to store mouse and keyboard events
mouse_events = []
keyboard_events = []

# Event logging functions
def on_click(x, y, button, pressed):
    timestamp = time.time()
    event = {
        'type': 'Pressed' if pressed else 'Released',
        'x': x,
        'y': y,
        'button': str(button),
        'timestamp': timestamp
    }
    mouse_events.append(event)

def on_move(x, y):
    timestamp = time.time()
    event = {
        'type': 'Move',
        'x': x,
        'y': y,
        'timestamp': timestamp
    }
    mouse_events.append(event)

def on_scroll(x, y, dx, dy):
    timestamp = time.time()
    event = {
        'type': 'Scroll',
        'x': x,
        'y': y,
        'dx': dx,
        'dy': dy,
        'timestamp': timestamp
    }
    mouse_events.append(event)

def on_key_press(key):
    timestamp = time.time()
    event = {
        'type': 'Pressed',
        'key': str(key),
        'timestamp': timestamp
    }
    keyboard_events.append(event)

def on_key_release(key):
    timestamp = time.time()
    event = {
        'type': 'Released',
        'key': str(key),
        'timestamp': timestamp
    }
    keyboard_events.append(event)
    # Stop listener if 'q' is pressed
    if key == pynput_keyboard.Key.esc:
        return False

# Functions to start listeners
def start_mouse_listener():
    with mouse.Listener(on_click=on_click, on_move=on_move, on_scroll=on_scroll) as listener:
        listener.join()

def start_keyboard_listener():
    with pynput_keyboard.Listener(on_press=on_key_press, on_release=on_key_release) as listener:
        listener.join()

# Start the mouse and keyboard listeners in separate threads
mouse_thread = threading.Thread(target=start_mouse_listener)
keyboard_thread = threading.Thread(target=start_keyboard_listener)
mouse_thread.start()
keyboard_thread.start()

print("Recording... Press 'q' to stop.")

try:
    while True:
        # Capture the screen
        img = pyautogui.screenshot()

        # Convert the screenshot to a numpy array
        frame = np.array(img)

        # Convert it from RGB to BGR (OpenCV uses BGR)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the frame to the video file
        out.write(frame)

        # Stop recording when 'q' is pressed
        if keyboard.is_pressed('q'):
            print("Recording stopped.")
            break

        # Small delay to reduce CPU usage
        time.sleep(0.01)

finally:
    # Release the video file when recording is stopped
    out.release()
    cv2.destroyAllWindows()

    # Stop the listeners
    # (pynput listeners stop when their callback functions return False)

    # Save the events to log files for further processing
    with open('mouse_events.json', 'w') as f:
        json.dump(mouse_events, f, indent=4)

    with open('keyboard_events.json', 'w') as f:
        json.dump(keyboard_events, f, indent=4)

    print("Mouse and keyboard events saved.")



