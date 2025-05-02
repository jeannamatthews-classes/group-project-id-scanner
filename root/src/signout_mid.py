from flask import Flask
from flask_apscheduler import APScheduler
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

class Config:
    SCHEDULER_API_ENABLED = True

app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

DATABASE = 'data.db'

def auto_checkout():
    print("Running auto-checkout...")
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Finds the students who checked in but never checked out
    cursor.execute("""
        SELECT id FROM checkins
        WHERE checkout_time IS NULL
    """)
    rows = cursor.fetchall()

    for row in rows:
        record_id = row[0]
        fake_checkout_time = datetime.now().replace(hour=23, minute=59, second=0, microsecond=0)
        cursor.execute("""
            UPDATE checkins
            SET checkout_time = ?
            WHERE id = ?
        """, (fake_checkout_time, record_id))
    
    conn.commit()
    conn.close()
    print("Auto-checkout complete.")

# Schedules the job to run daily at midnight
scheduler.add_job(id='AutoCheckoutJob', func=auto_checkout, trigger='cron', hour=0, minute=0)
