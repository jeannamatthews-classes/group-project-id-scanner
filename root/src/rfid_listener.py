# src/rfid_listener.py
"""
RFID listener using USB input device
------------------------------------------
• Opens the /kiosk page in a browser
• Listens for RFID scans.
• Tells server to update the action queue.
"""

import requests
from evdev import InputDevice, categorize, ecodes, list_devices
from app import app
from tables import User, Scans, db

# important: Use Pi's local ip address (Not localhost if controlling remotely)
BASE_URL = "http://128.153.180.68:5000"  # Use 127.0.0.1 if running directly on Pi

# Find USB device whose name contains "HID"
def find_rfid_device():
    for path in list_devices():
        device = InputDevice(path)
        if "HID" in device.name:
            return device
    return None

# Read badge scans from the device
def read_rfid(device):
    rfid = ""
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            keyevent = categorize(event)
            if keyevent.keystate == 1:  # Key down
                keycode = keyevent.keycode
                if isinstance(keycode, list):
                    keycode = keycode[0]
                if keycode == 'KEY_ENTER':
                    yield rfid
                    rfid = ""
                else:
                    digit = keycode.replace('KEY_', '')
                    if digit.isdigit():
                        rfid += digit

def main() -> None:
    device = find_rfid_device()
    if not device:
        print("RFID reader not found. Please check USB connection.")
        return

    print("RFID Listener - waiting for badge scans...")

    for rfid in read_rfid(device):
        print(f"Scanned RFID: {rfid}")

        with app.app_context():
            user = db.session.get(User, rfid)
            if user:
                open_visit = Scans.query.filter_by(rfid=rfid, time_out=None).first()
                action_type = "scan_out" if open_visit else "scan_in"
            else:
                action_type = "register"

        payload = {"rfid": rfid, "type": action_type}
        try:
            response = requests.post(f"{BASE_URL}/api/trigger_action", json=payload)
            print(f"→ queued {action_type} for {rfid} - Server responded {response.status_code}")
        except Exception as err:
            print("Could not contact server:", err)
        
if __name__ == "__main__":
    main()
