"""
rfid_listener 

Listens for RFID scans & triggers the web interface

NOTE: Before connecting to the pi, scans will be simulated in another script
"""

import sys
from datetime import datetime
from app import app  # Import the Flask app instance from your app.py
from tables import db, User, Scans, Machine

def simulate_new_user(rfid):
    """
    Simulates new user registration.
    Prompts for the new user details, creates the user in the database, and logs a scan-in event.
    """
    print(f"RFID {rfid} not found. Registering as a new user.")
    # Prompt for new user details
    student_id = input("Enter student ID: ").strip()
    username = input("Enter username: ").strip()
    first_name = input("Enter first name: ").strip()
    last_name = input("Enter last name: ").strip()

    # Create a new User instance with the submitted data
    new_user = User(
        rfid=rfid,
        student_id=student_id,
        username=username,
        first_name=first_name,
        last_name=last_name
    )
    db.session.add(new_user)
    db.session.commit()
    print("New user registered.")

    # Log the scan in (create a new Scans row)
    scan_in(rfid)

def scan_in(rfid):
    """
    Logs a scan-in event by creating a new Scans row with the current time.
    The 'time_out' field remains NULL until the user scans out.
    """
    print(f"Logging scan-in for RFID {rfid}...")
    new_scan = Scans(
        rfid=rfid,
        date=datetime.today().date(),
        time_in=datetime.now().time()  # Only the time is stored
    )
    db.session.add(new_scan)
    db.session.commit()
    print("Scan-in logged.")

def scan_out(rfid):
    """
    Logs a scan-out event by updating an existing open Scans row.
    First, the open scan (with time_out NULL) is looked up.
    Then, the user is prompted for machine usage, and the scan record is updated.
    """
    print(f"Logging scan-out for RFID {rfid}...")
    open_scan = Scans.query.filter_by(rfid=rfid, time_out=None).first()
    if not open_scan:
        print("No open session found for this RFID. Cannot scan out.")
        return

    # Prompt for machine usage (simulate by entering comma-separated machine IDs)
    machine_input = input("Enter machine IDs used (comma-separated): ").strip()
    try:
        # Convert input to a list of integers
        machine_ids = [int(mid.strip()) for mid in machine_input.split(',') if mid.strip().isdigit()]
    except Exception as e:
        print("Invalid machine input. Aborting scan-out.")
        return

    # Query for the corresponding Machine objects
    machines = Machine.query.filter(Machine.id.in_(machine_ids)).all()

    # Update the open scan record with the current time and machine usage
    open_scan.time_out = datetime.now().time()
    open_scan.machines = machines
    db.session.commit()
    print("Scan-out logged.")

def main():
    """
    Main simulation loop.
    Displays a message indicating that the simulation is running, then repeatedly
    prompts for an RFID. It exits when the user types "exit".
    """
    # Create an application context to use the database
    with app.app_context():
        print("RFID Listener Simulation Running. Type 'exit' to quit.")
        while True:
            rfid = input("Enter RFID: ").strip()
            if rfid.lower() == "exit":
                print("Exiting simulation.")
                break

            # Determine what action to take based on the RFID
            user = User.query.get(rfid)
            if not user:
                # The RFID is not in the database: handle as new user registration and scan in
                simulate_new_user(rfid)
            else:
                # The user exists; check if there's an open scan event (time_out is NULL)
                open_scan = Scans.query.filter_by(rfid=rfid, time_out=None).first()
                if open_scan:
                    # User is already signed in; treat this as a scan-out event
                    scan_out(rfid)
                else:
                    # No open session found, so log a new scan-in event
                    scan_in(rfid)

if __name__ == "__main__":
    main()

