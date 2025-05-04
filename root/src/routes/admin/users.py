from flask import render_template, redirect, url_for, request, session
from . import admin_bp
from tables import db, User

@admin_bp.route("/users")
def view_users():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))
    users = User.query.all()
    return render_template("admin/users.html", users=users)

@admin_bp.route("/users/delete/<rfid>", methods=["POST"])
def delete_user(rfid):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin.login"))
    u = db.session.get(User, rfid)
    if u:
        db.session.delete(u)
        db.session.commit()
    return redirect(url_for("admin.view_users"))
