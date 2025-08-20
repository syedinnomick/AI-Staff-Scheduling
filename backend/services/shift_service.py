import datetime as dt
from backend.models.shift import Shift
from backend.db.connection import db

class ShiftService:
    def create(self, date: dt.date, time: str, staff_id: int | None) -> Shift:
        shift = Shift(date=date, time=time, staff_id=staff_id)
        db.session.add(shift)
        db.session.commit()
        return shift

    def list(self) -> list[Shift]:
        return Shift.query.order_by(Shift.date.asc(), Shift.time.asc()).all()

    def clear_all(self) -> int:
        count = Shift.query.delete()
        db.session.commit()
        return count
