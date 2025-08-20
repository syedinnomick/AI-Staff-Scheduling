from flask import Blueprint, jsonify, request
import datetime as dt
from backend.services.schedule_service import ScheduleService

schedule_bp = Blueprint("schedule", __name__)
_service = ScheduleService()

class ScheduleRoutes:
    @staticmethod
    @schedule_bp.route("/generate-schedule", methods=["POST"])
    def generate():
        payload = request.get_json(force=True) or {}
        start = payload.get("start_date")
        days = int(payload.get("days", 7))
        start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
        try:
            out = _service.generate(start_date=start_date, days=days)
            return jsonify(out), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400

    @staticmethod
    @schedule_bp.route("/view-schedule", methods=["GET"])
    def view():
        return jsonify(_service.view()), 200
