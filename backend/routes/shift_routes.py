from flask import Blueprint, jsonify
from backend.services.shift_service import ShiftService

shift_bp = Blueprint("shift", __name__)
_service = ShiftService()

class ShiftRoutes:
    @staticmethod
    @shift_bp.route("/shifts", methods=["GET"])
    def list_all():
        return jsonify([s.to_dict() for s in _service.list()]), 200

    @staticmethod
    @shift_bp.route("/shifts/clear", methods=["POST"])
    def clear_all():
        count = _service.clear_all()
        return jsonify({"deleted": count}), 200
