# src/routes/admin/machines.py
from flask import Blueprint, render_template, request, redirect, url_for
from tables import db, Machine
from . import admin_bp

@admin_bp.route("/machines")
def view_machines():
    machines = Machine.query.order_by(Machine.name).all()
    return render_template("admin/machines.html", machines=machines)

@admin_bp.route("/machines/add", methods=["POST"])
def add_machine():
    name = request.form.get("name")
    if name:
        existing = Machine.query.filter_by(name=name).first()
        if not existing:
            db.session.add(Machine(name=name))
            db.session.commit()
    return redirect(url_for("admin.view_machines"))

@admin_bp.route("/machines/delete/<int:id>", methods=["POST"])
def delete_machine(id):
    machine = db.session.get(Machine, id)
    if machine:
        db.session.delete(machine)
        db.session.commit()
    return redirect(url_for("admin.view_machines"))
