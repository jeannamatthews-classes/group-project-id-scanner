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

def spawn(cmd, *, background=False):
    """Helper to run a command relative to project root."""
    full = [sys.executable, str(BASE_DIR / cmd)]
    if background:
        return subprocess.Popen(full)
    else:
        subprocess.run(full, check=True)

def main():
    # 1. Add machines
    spawn("src/populate_machines.py")

    # 2. Start Flask
    flask_proc = spawn("src/app.py", background=True)
    time.sleep(2)  # wait for server to bind

    try:
        # 3. Run RFID listener (blocking)
        spawn("src/rfid_listener.py")
    finally:
        # 4. Kill Flask when listener exits or on Ctrl‑C
        flask_proc.terminate()
        flask_proc.wait()

if __name__ == "__main__":
    main()
