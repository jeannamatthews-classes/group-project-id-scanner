# ID Scanner Project

## 📦 Project Overview

This document outlines the hardware setup for the **ID Scanner project**, which aims to create an easier check-in/check-out system for the **Clarkson MakerSpace**. 
The primary goal is to replace the existing inefficient Google Form sign-in process. The system will use RFID technology to identify users and track their entry, exit, and machine usage.

## 👨‍👦‍👦 Team
- **Nicholas Sheldon** 
- **Hunter Smith** 
- **Delara Panahi**
- **Samantha Sikora**
- **Soliat Adeboye** 

## Features 
-  **Scan-In/Out:** Quick and easy entry/exit logging using student IDs
-  **Machine Usage Tracking:** At scan-out, students select machines used via a simple interface
-  **Database:** Records timestamped scan-in and scan-out events for each student 
-  **Basic Admin Dashboard (MVP):** View logs and potentially generate basic usage reports (CSV exports)
-  **SSH Operation:** Designed to run without a monitor, keyboard, and mouse after initial setup

**Stretch Goals (Beyond MVP):**
-   Integration with university systems (e.g., pulling student email/name) 
-   Real-time crowd meter or machine usage display 
  
## 🛠️ Technical Stack
This project uses a mix of hardware and software components:

  **Hardware:**

| Component              | Description                                  |
|------------------------|-----------------------------------------------|
| Raspberry Pi 4         | Main computing unit       |
| MicroSD/USB Drive      | Bootable OS storage (Raspberry Pi OS)         |
| HID-compatible 125KHz RFID USB reader     | For card/tag scanning      |
| Monitor & Mirco-HDMI (initial setup) | Used for configuring the Pi initially   |
| Power Supply (USB-C)   | Standard Pi power input                       |
| Touchscreen Device     | For displaying the webpage                    |

 **Software:**
 - **Operating System:** Raspberry Pi OS
 - **Backend:** **Python** with the **Flask** framework for handling RFID input, database interactions, and serving the UI
 - **Database:** **SQLAlchemy** for local storage of student data, session logs, and machine usage
 - **Frontend/UI:** **HTML/CSS** scan-in/out interface. Designed to be accessed via a web browser (e.g., on an iPad) 

## ⚙️ Setup Instructions and Installation (this is a detailed version of the deployment doc)

Follow these steps to get the system running:

1.  **Prepare Raspberry Pi OS:**
    *   Flash Raspberry Pi OS onto a **USB drive/SD Card** using the Raspberry Pi Imager 
    *   During image customization, **enable SSH**, set a hostname, and user credentials  This is saved to the USB drive, so it carries over if you switch Pi hardware.
    *   (Optional but recommended) Configure **Wi-Fi details** by creating a `wpa_supplicant.conf` file in the `boot` partition of the USB drive *before* the first boot.
    *   Perform the first boot connected to a monitor/keyboard to ensure everything starts correctly 
2.  **Enable Remote Access (Optional but useful):**
    *   **SSH:** Should be enabled from OS setup
    *   **RDP (Optional):** Install via `sudo apt install xrdp -y` for a remote desktop GUI session 
3.  **Connect the USB RFID Reader:**
    *   Simply **plug the 125KHz HID USB RFID reader into an available USB port** on the Raspberry Pi. 
4.  **Install Required Software:**
    *   Update package list: `sudo apt update` 
    *   Install Python and pip (usually included).
    *   Install Flask: `pip install Flask` 
    *   Install SQLite (should be included, but confirm): `sudo apt install sqlite3` 
    *   Install any necessary Python libraries to **capture USB/keyboard input** if your chosen reader requires a specific method beyond standard input reading. 
5.  **Clone Repository:**
    - `git clone https://github.com/jeannamatthews-classes/group-project-id-scanner.git`
    - `cd group-project-id-scanner`
6.  **Create and Activate Virtual Environment**
    - `python3 -m venv env`
    - `source env/bin/activate`
7.  **Install Requirements**
    `pip install -r root/requirements.txt`
8.  **Run the Application:**
    *   Navigate to the project directory `cd root`
    *   Start the Flask backend application (`python run_kiosk.py`). 
    *   The Flask app will serve the web UI locally on the Pi on port 5000.

## Dependencies

- **Flask**: Web framework used for the backend.
- **SQLAlchemy**: ORM for database interactions.
- **evdev**: For handling USB device input (may be needed for certain RFID readers).
- **Flask-APScheduler**: For scheduling tasks like auto sign-out.

## 🌐 Accessing the Web App

When the Flask app is running on the Raspberry Pi:

1. Find the Raspberry Pi’s IP address on your Wi-Fi network.
2. On the iPad (or any device on the same network), open a web browser.
3. Go to `http://[Raspberry_Pi_IP_Address]:5000/kiosk`.
4. When an ID is scanned, you should see the check-in/check-out screen.

## 📊 Documentation

The `docs/` directory contains important project documentation

-  `docs/design/`: Has design documents like the initial proposal, the main Design Document PDF, which includes flowcharts, mock-up UIs, and schema diagrams.
-  `docs/planning/`: Includes weekly Gantt charts and notes on risks or schedule changes. Each week has its own folder (e.g., `20250303`, `20250317`).
-  `docs/timelog/`: Stores each team member’s timelog. Everyone has a file with their username (e.g., `username.txt`), showing what they worked on.

## 🔑 RFID Frequency

This system uses **125KHz HID-compatible RFID tags** to scan student IDs. Please ensure that your RFID cards/tags are compatible with the HID H10301 format to ensure correct functionality.

## Troubleshooting
- **Problem:** Raspberry Pi doesn’t boot properly.
  - **Solution:** Double-check the power supply and make sure the Raspberry Pi OS is correctly flashed onto your SD card/USB. If using Wi-Fi, ensure your `wpa_supplicant.conf` file is set up properly.
  
- **Problem:** The RFID reader isn't scanning properly.
  - **Solution:** Ensure that the RFID reader is plugged in correctly. Use the `lsusb` command to check if the Pi recognizes the device.

### Please refer to the maintenance plan in the docs directory for additional help

# In Progress / Future Work
- **University System Integration**: In the future, we plan to integrate with Clarkson's student database to automate user identification and simplify the check-in process.
- **Real-time Machine Usage**: We're exploring options to add a live machine status display, showing which machines are in use and which are available in real-time.

