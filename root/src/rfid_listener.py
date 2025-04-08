"""
rfid_listener.py

Simulated RFID Listener using Flask's test client.
This script accepts RFID inputs from the command line, queries the database,
and then calls the appropriate endpoints in your scans and users routes.

No web browsers are opened; this fully simulates the HTTP calls that would occur
in a production system.
"""

import sys
from app import app  # Import the Flask app instance from your app.py
from tables import db, User, Scans  # Import the database and models

def process_rfid(rfid):
    with app.app_context():
        user = User.query.get(rfid)
    
    with app.test_client() as client:
        if user:
            with app.app_context():
                open_visit = Scans.query.filter_by(rfid=rfid, time_out=None).first()
            if open_visit:
                # Simulate a scan_out: perform a GET request to the scan_out endpoint.
                response = client.get(f"/scan/out/{rfid}")
            else:
                # Simulate a scan_in: perform a POST request to the scan_in endpoint.
                response = client.post(f"/scan/in/{rfid}")
        else:
            # User does not exist: simulate accessing the new user registration page.
            response = client.get(f"/users/new?rfid={rfid}")
        
        # Print only minimal output (e.g., the status code) to simulate processing.
        print(f"Processed RFID {rfid}: HTTP {response.status_code}")

def main():
    """
    Main loop: repeatedly prompts for an RFID.
    Type "exit" to terminate the simulation.
    """
    print("RFID Listener Simulation Running (no browsers will open).")
    print("Type an RFID value or 'exit' to quit.")
    while True:
        rfid = input().strip()
        if rfid.lower() == "exit":
            print("Exiting simulation.")
            break
        process_rfid(rfid)

if __name__ == "__main__":
    main()
