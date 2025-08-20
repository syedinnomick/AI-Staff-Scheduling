from backend.models.staff import Staff
from backend.db.connection import db

class StaffService:
    def create(self, data: dict) -> Staff:
        staff = Staff(
            name=data["name"],
            role=data["role"],
            specialty=data.get("specialty"),
            availability=data.get("availability"),
        )
        db.session.add(staff)
        db.session.commit()
        return staff

    def list(self) -> list[Staff]:
        return Staff.query.order_by(Staff.id.asc()).all()

    def get(self, staff_id: int) -> Staff | None:
        return Staff.query.get(staff_id)

    def update(self, staff_id: int, data: dict) -> Staff | None:
        staff = Staff.query.get(staff_id)
        if not staff:
            return None
        staff.name = data.get("name", staff.name)
        staff.role = data.get("role", staff.role)
        staff.specialty = data.get("specialty", staff.specialty)
        staff.availability = data.get("availability", staff.availability)
        db.session.commit()
        return staff

    def delete(self, staff_id: int) -> bool:
        staff = Staff.query.get(staff_id)
        if not staff:
            return False
        db.session.delete(staff)
        db.session.commit()
        return True
