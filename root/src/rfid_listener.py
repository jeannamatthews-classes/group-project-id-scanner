"""
rfid_listener.py

Simulated RFID Listener using Flask's test client.
This script accepts RFID inputs from the command line, queries the database,
and then calls the appropriate endpoints in your scans and users routes.

No web browsers are opened; this fully simulates the HTTP calls that would occur
in a production system.
"""

import sys
import webbrowser
from app import app  # Import the Flask app instance from your app.py
from tables import db, User, Scans  # Import the database and models

# Base url of running Flask server
BASE_URL = "http://localhost:5000"

def process_rfid(rfid):
    """
    Queries the db for the rfid
        if rfid exists
            if no open session exists, open scan-in URL?
            else opens scan-out URL
        else open new member registration page
    """
    with app.app_context():
         user = User.query.get(rfid)
         open_visit = None
         if user:
             open_visit = Scans.query.filter_by(rfid=rfid, time_out=None).first()
    
    if user:
        with app.app_context():
            if open_visit:
                url = f"{BASE_URL}/scan/out/{rfid}"
                print("Opening scanning out page")
            else:
                url = f"{BASE_URL}/scan/in/{rfid}"
                print("Opening scan in page")   #This should just be index.html
    else:
        #rfid not found
        url = f"{BASE_URL}/users/new?rfid={rfid}"
        print("Opening new member registration page")
    webbrowser.open(url)
    
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
