from backend.db.connection import db

class Staff(db.Model):
    __tablename__ = "staff"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), nullable=False)        # e.g., doctor, nurse
    specialty = db.Column(db.String(50), nullable=True)    # e.g., ICU, OR, ER
    availability = db.Column(db.String(500), nullable=True)  # JSON string (optional)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "specialty": self.specialty,
            "availability": self.availability,
        }
