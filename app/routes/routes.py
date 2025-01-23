from flask import Blueprint, jsonify, request, Depends
from ..database import SessionLocal
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Define the Blueprint
main_bp = Blueprint('main', __name__)

# Home route
@main_bp.route('/home')
def home():
    """
    Home route for the application.
    """
    return jsonify({"message": "Welcome to the Notification Service!"})

# Dummy notifications route
@main_bp.route('/', methods=['GET'])
def get_notifications(db: SessionLocal = Depends(get_db)):
    """
    Route to fetch all notifications (Dummy response for now).
    """
    notifications = db.query(Notification).all()
    return notifications
    # dummy_notifications = [
    #     {"id": 1, "message": "First notification", "type": "info", "read": False},
    #     {"id": 2, "message": "Second notification", "type": "alert", "read": True},
    # ]
    # return jsonify(dummy_notifications)

# Fetch notifications for a specific patient
@main_bp.route('/patient/<string:patient_id>', methods=['GET'])
def get_notifications_by_patient(patient_id):
    """
    Fetch notifications for a specific patient (Dummy response for now).
    """
    dummy_notifications = [
        {"id": 1, "message": "Patient notification 1", "type": "info", "patient_id": patient_id, "read": False},
        {"id": 2, "message": "Patient notification 2", "type": "alert", "patient_id": patient_id, "read": True},
    ]
    return jsonify(dummy_notifications)

# Fetch notifications for a specific doctor
@main_bp.route('/doctor/<string:doctor_id>', methods=['GET'])
def get_notifications_by_doctor(doctor_id):
    """
    Fetch notifications for a specific doctor (Dummy response for now).
    """
    dummy_notifications = [
        {"id": 1, "message": "Doctor notification 1", "type": "info", "doctor_id": doctor_id, "read": False},
        {"id": 2, "message": "Doctor notification 2", "type": "alert", "doctor_id": doctor_id, "read": True},
    ]
    return jsonify(dummy_notifications)

# Update read status of a notification
@main_bp.route('/<int:notification_id>', methods=['PATCH'])
def mark_notification_as_read(notification_id):
    """
    Update read status of a notification (Dummy response for now).
    """
    data = request.get_json()
    read_status = data.get('read')

    if read_status is None:
        return jsonify({"error": 'The "read" field is required.'}), 400

    # Simulate updating a notification
    updated_notification = {
        "id": notification_id,
        "read": read_status,
        "message": f"Notification {notification_id} updated.",
    }
    return jsonify(updated_notification), 200
