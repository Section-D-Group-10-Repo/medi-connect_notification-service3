from flask import Blueprint, jsonify

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
    Route to fetch notifications.
    (Dummy response for now; integrate with database later)
    """
    dummy_notifications = [
        {"id": 1, "message": "First notification", "type": "info"},
        {"id": 2, "message": "Second notification", "type": "alert"},
        {"id": 3, "message": "Second notification", "type": "alert"},
    ]
    return jsonify(dummy_notifications)
