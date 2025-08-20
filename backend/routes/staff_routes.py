from flask import Blueprint, jsonify, request
from backend.services.staff_service import StaffService

staff_bp = Blueprint("staff", __name__)
_service = StaffService()

class StaffRoutes:
    @staticmethod
    @staff_bp.route("/staff", methods=["POST"])
    def create():
        staff = _service.create(request.get_json(force=True))
        return jsonify(staff.to_dict()), 201

    @staticmethod
    @staff_bp.route("/staff", methods=["GET"])
    def list_all():
        return jsonify([s.to_dict() for s in _service.list()]), 200

    @staticmethod
    @staff_bp.route("/staff/<int:staff_id>", methods=["GET"])
    def get(staff_id: int):
        s = _service.get(staff_id)
        if not s:
            return jsonify({"error": "Not found"}), 404
        return jsonify(s.to_dict()), 200

    @staticmethod
    @staff_bp.route("/staff/<int:staff_id>", methods=["PUT"])
    def update(staff_id: int):
        s = _service.update(staff_id, request.get_json(force=True))
        if not s:
            return jsonify({"error": "Not found"}), 404
        return jsonify(s.to_dict()), 200

    @staticmethod
    @staff_bp.route("/staff/<int:staff_id>", methods=["DELETE"])
    def delete(staff_id: int):
        ok = _service.delete(staff_id)
        return (jsonify({"message": "Deleted"}), 200) if ok else (jsonify({"error": "Not found"}), 404)
 