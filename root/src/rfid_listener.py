# src/rfid_listener.py
"""
CLI “badge reader” used during development
-----------------------------------------
• Opens the /kiosk page in a browser one time.
• Waits for you to type an RFID number at the prompt.
• Looks up that RFID in the database:
    - new card      → action = register
    - known, no open visit → action = scan_in
    - known, open visit    → action = scan_out
• Sends a JSON packet to /api/trigger_action.
The kiosk page then switches its iframe accordingly.
"""

import webbrowser                 # to launch the kiosk page
import requests                   # to hit the Flask JSON API
from app import app               # Flask application (for DB context)
from tables import User, Scans, db  # ORM models + session

BASE_URL = "http://localhost:5000"   # where Flask is listening


def main() -> None:
    """Simple REPL that turns typed numbers into queue actions."""
    # Launch the kiosk in the default browser (one tab, reused)
    webbrowser.open(f"{BASE_URL}/kiosk", new=0, autoraise=True)
    print("RFID Listener Simulation - type an RFID or 'exit'.")

    while True:
        rfid = input("RFID> ").strip()      # read rfid number
        if rfid.lower() == "exit":          # quit command
            print("Goodbye.")
            break
        if not rfid:                        # ignore blank lines
            continue

        # Decide what should happen for this rfid
        with app.app_context():
            user = db.session.get(User, rfid)                 # Primary key lookup
            if user:
                open_visit = Scans.query.filter_by(
                    rfid=rfid, time_out=None
                ).first()                                     # open session?
                action_type = "scan_out" if open_visit else "scan_in"
            else:
                action_type = "register"

        # Ship the instruction to the Flask API
        payload = {"rfid": rfid, "type": action_type}
        try:
            requests.post(f"{BASE_URL}/api/trigger_action", json=payload)
            print(f"→ queued {action_type} for {rfid}")
        except Exception as err:
            print("Could not contact server:", err)


if __name__ == "__main__":
    main()
