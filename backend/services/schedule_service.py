import datetime as dt
from collections import defaultdict
from backend.models.staff import Staff
from backend.models.shift import Shift
from backend.db.connection import db

class ScheduleService:
    """
    Week-2 basic generator:
    - Inputs: start_date, days
    - Constraints:
      * Each staff max 1 shift per day (no double booking)
      * Round-robin assignment to balance load
      * Alternate day/night per staff across days for crude fairness
    """
    def generate(self, start_date: dt.date, days: int = 7) -> list[dict]:
        staff = Staff.query.order_by(Staff.id.asc()).all()
        if not staff:
            raise ValueError("No staff available")

        # clear existing for the interval (simple POC behavior)
        end_date = start_date + dt.timedelta(days=days)
        Shift.query.filter(Shift.date >= start_date, Shift.date < end_date).delete()

        # Track last shift type per staff to alternate
        last_type: dict[int, str] = defaultdict(lambda: "night")
        created: list[Shift] = []
        staff_idx = 0
        staff_count = len(staff)

        for d in range(days):
            day = start_date + dt.timedelta(days=d)
            # Two shifts per day for POC: day & night
            # Assign different people to day and night; wrap round-robin
            for _slot in ("day", "night"):
                assignee = staff[staff_idx % staff_count]
                # ensure at most one shift per day per staff
                # if last chosen already got a shift today, move pointer
                attempts = 0
                while any(s.staff_id == assignee.id and s.date == day for s in created) and attempts < staff_count:
                    staff_idx += 1
                    assignee = staff[staff_idx % staff_count]
                    attempts += 1

                # Alternate type for the assignee for crude fairness
                next_type = "day" if last_type[assignee.id] == "night" else "night"
                shift_type = next_type if _slot == next_type else _slot
                created.append(Shift(date=day, time=shift_type, staff_id=assignee.id))
                last_type[assignee.id] = shift_type
                staff_idx += 1

        db.session.add_all(created)
        db.session.commit()
        return [s.to_dict() for s in created]

    def view(self) -> list[dict]:
        return [s.to_dict() for s in Shift.query.order_by(Shift.date.asc(), Shift.time.asc()).all()]
