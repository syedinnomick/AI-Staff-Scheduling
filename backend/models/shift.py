from backend.db.connection import db

class Shift(db.Model):
    __tablename__ = "shifts"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(20), nullable=False)  # "day" | "night"
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=True)

    staff = db.relationship("Staff", backref="shifts", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "time": self.time,
            "staff_id": self.staff_id,
        }
