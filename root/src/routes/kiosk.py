# src/routes/kiosk.py
"""
kiosk.py - tiny “traffic-control” layer
--------------------------------------
• /kiosk                : full-screen shell the iPad loads once
• /api/trigger_action   : RFID listener drops a JSON command here
• /api/next_action      : kiosk polls; gets the next command
• /api/ack_action       : kiosk tells server “handled, pop queue”
The queue lives in RAM (good enough for a single Pi).
"""

from flask import Blueprint, render_template, request, jsonify  # flask helpers

action_queue: list[dict] = []          # FIFO of pending screen actions

kiosk_bp = Blueprint("kiosk", __name__)  # blueprint for these routes


@kiosk_bp.route("/kiosk")
def kiosk():
    return render_template("kiosk.html")  # send the iframe shell


@kiosk_bp.route("/api/trigger_action", methods=["POST"])
def trigger_action():
    data = request.get_json() or {}      # JSON from RFID listener
    action_queue.append(data)            # push onto queue
    return ("", 204)                     # 204 = success, no content


@kiosk_bp.route("/api/next_action")
def next_action():
    # return first item or {"type":"none"} so kiosk JS can decide
    return jsonify(action_queue[0] if action_queue else {"type": "none"})


@kiosk_bp.route("/api/ack_action", methods=["POST"])
def ack_action():
    if action_queue:
        action_queue.pop(0)              # drop the item we just showed
    return ("", 204)
