import logging
import re
from flask import jsonify

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def success_response(data, status=200):
    """
    Return a standardized success JSON response.
    """
    return jsonify({"success": True, "data": data}), status

def error_response(message, status=400):
    """
    Return a standardized error JSON response.
    """
    return jsonify({"success": False, "error": message}), status

def validate_email(email):
    """
    Validate an email address using regex.
    """
    email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
    return re.match(email_regex, email) is not None

def validate_phone_number(phone):
    """
    Validate a phone number using regex.
    Ensures the phone number contains only digits and optional + at the start.
    """
    phone_regex = r"^\+?[0-9]{7,15}$"
    return re.match(phone_regex, phone) is not None

def safe_db_commit(session, action="commit"):
    """
    Safely commit changes to the database, with error handling.
    :param session: SQLAlchemy session
    :param action: The type of database action (default: 'commit')
    """
    try:
        session.commit()
        logger.info(f"Database {action} successful.")
    except Exception as e:
        session.rollback()
        logger.error(f"Database {action} failed: {e}")
        raise
