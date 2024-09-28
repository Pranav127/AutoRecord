import json
import time
import pyautogui
import threading

# Load mouse and keyboard events
with open('mouse_events.json', 'r') as f:
    mouse_events = json.load(f)

with open('keyboard_events.json', 'r') as f:
    keyboard_events = json.load(f)

# Combine the logs
all_events = mouse_events + keyboard_events

# Sort events by their timestamp
all_events.sort(key=lambda event: event['timestamp'])

# Get the time difference between events to replay them accurately
start_time = all_events[0]['timestamp']
current_time = time.time()

# Calculate the time offset
time_offset = current_time - start_time

print("Replaying actions...")

# Function to replay events
def replay_events():
    for event in all_events:
        # Calculate the exact time to perform the event
        event_time = event['timestamp'] + time_offset
        time_to_wait = event_time - time.time()
        if time_to_wait > 0:
            time.sleep(time_to_wait)

        # Replaying Mouse Events
        if 'x' in event and 'y' in event:
            x, y = event['x'], event['y']
            if event['type'] == 'Move':
                pyautogui.moveTo(x, y, duration=0)
            elif event['type'] == 'Pressed':
                button = 'left' if 'left' in event['button'] else 'right'
                pyautogui.moveTo(x, y, duration=0)
                pyautogui.mouseDown(button=button)
            elif event['type'] == 'Released':
                button = 'left' if 'left' in event['button'] else 'right'
                pyautogui.mouseUp(button=button)
            elif event['type'] == 'Scroll':
                pyautogui.scroll(event.get('dy', 0), x=x, y=y)

        # Replaying Keyboard Events
        elif 'key' in event:
            key = event['key'].replace("'", "").replace('Key.', '')
            if event['type'] == 'Pressed':
                if len(key) > 1:  # Special keys
                    pyautogui.keyDown(key)
                else:
                    pyautogui.press(key)
            elif event['type'] == 'Released':
                if len(key) > 1:
                    pyautogui.keyUp(key)

print("Starting in 5 seconds...")
time.sleep(5)  # Give the user time to switch to the application

replay_thread = threading.Thread(target=replay_events)
replay_thread.start()
replay_thread.join()

print("Replay finished.")
