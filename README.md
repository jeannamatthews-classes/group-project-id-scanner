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
-   **Scan-In/Out:** Quick and easy entry/exit logging using student IDs
-   **Machine Usage Tracking:** At scan-out, students select machines used via a simple interface
-  **Database:** Records timestamped scan-in and scan-out events for each student 
-   **Basic Admin Dashboard (MVP):** View logs and potentially generate basic usage reports (CSV exports)
-   **SSH Operation:** Designed to run without a monitor, keyboard, and mouse after initial setup

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




In Progress...

