from flask import Blueprint, render_template, redirect, url_for, request
from tables import db, User

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/users")
def users():
    all_users = User.query.all()
    return render_template("admin_users.html", users=all_users)

@admin_bp.route("/delete_user/<rfid>", methods=["POST"])
def delete_user(rfid):
    user = db.session.get(User, rfid)
    if user:
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for("admin.users"))

@admin_bp.route("/auto_signed_out")
def auto_signed_out():
    from tables import Scans, User
    from sqlalchemy.orm import joinedload

    scans = Scans.query.options(joinedload(Scans.machines))\
        .filter(Scans.was_auto_signed_out == True)\
        .order_by(Scans.date.desc(), Scans.time_in.desc()).all()

    # Attach user to each scan manually (since rfid is foreign key)
    users = {u.rfid: u for u in User.query.all()}
    return render_template("admin_autosign.html", scans=scans, users=users)

