from app import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String(255), nullable=False)
    doctor_id = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    message = db.Column(db.String(1024), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    # read = db.Column(db.Boolean, default=False, nullable=False)  # New attribute

    def __repr__(self):
        return f"<Notification id={self.id}, patient_id={self.patient_id}, message={self.message}, read={self.read}>"