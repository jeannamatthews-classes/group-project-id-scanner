from flask_apscheduler import APScheduler
from datetime import datetime, time
from tables import db, Scans

def auto_sign_out():
    from app import app  # import here to avoid circular issues
    with app.app_context():
        today = datetime.now().date()
        open_scans = Scans.query.filter(Scans.time_out == None, Scans.date < today).all()
        for scan in open_scans:
            scan.time_out = time(23, 59, 59)
            scan.was_auto_signed_out = True
            print(f"Auto-signed out RFID {scan.rfid} on {scan.date}")
        db.session.commit()

def setup_scheduler(app):
    scheduler = APScheduler()
    scheduler.init_app(app)
    scheduler.start()
    scheduler.add_job(
        id='AutoSignOutJob',
        func=auto_sign_out,
        trigger='cron',
        hour=0,
        minute=0
    )
