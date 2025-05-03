"""
run_kiosk.py
Starts:
  1) populate_machines.py (once)
  2) app.py  (Flask server)   - background
  3) rfid_listener.py         - foreground
When the listener exits, the Flask process is terminated.
"""
import subprocess, time, sys, signal, os, pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent

def main():
    # 1. Add machines
    subprocess.run([sys.executable, str(BASE_DIR / "src/populate_machines.py")], check=True) 

    # 2. Start Flask
    flask_proc = subprocess.Popen([sys.executable, str(BASE_DIR / "src/app.py")]) 
    time.sleep(2)  # wait for server to bind

    try:
        # 3. Run RFID listener (blocking)
        subprocess.run([sys.executable, str(BASE_DIR / "src/rfid_listener.py")], check=True) 
    finally:
        # 4. Kill Flask when listener exits or on Ctrl‑C
        flask_proc.terminate()
        flask_proc.wait()

if __name__ == "__main__":
    main()
