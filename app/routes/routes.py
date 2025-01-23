from flask import Blueprint, jsonify
# from app.models import Notification
from .. import db
from ..models.models import Notification

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Home route for the application.
    """
    return jsonify({"message": "Welcome to the Notification Service!"})

@main_bp.route('/notifications', methods=['GET'])
def notifications():
    """
    Route to fetch notifications from the database.
    """
    try:
        notifications = Notification.query.all()
        notifications_list = [
            {
                "id": n.id,
                "patient_id": n.patient_id,
                "doctor_id": n.doctor_id,
                "message": n.message,
                "type": n.type,
                "read": n.read,
                "created_at": n.created_at,
                "updated_at": n.updated_at,
            }
            for n in notifications
        ]
        return jsonify(notifications_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main_bp.route('/test_db')
def test_db():
    try:
        # Example query to check if the database is working
        test_notification = Notification.query.first()
        if test_notification:
            return f"Found notification: {test_notification}", 200
        else:
            return "No notifications found.", 404
    except Exception as e:
        return f"Error accessing database: {e}", 500
