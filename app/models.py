from app import db

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.String, nullable=True)  # Patient ID (optional)
    doctor_id = db.Column(db.String, nullable=True)   # Doctor ID (optional)
    message = db.Column(db.String, nullable=False)    # Notification message
    type = db.Column(db.String, nullable=False)       # Notification type
    read = db.Column(db.Boolean, default=False)       # Read status
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())  # Creation timestamp
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp()) # Update timestamp

    def __repr__(self):
        return f"<Notification {self.id}>"
