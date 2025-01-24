![Uploading image.png…]()

# Medi-Connect Notifications

Medi-Connect Notifications is a microservice designed to handle notifications for patients and doctors in a healthcare system. It consumes messages from a RabbitMQ queue, processes them, and sends notifications (e.g., emails) to the respective recipients. Notifications are also stored in a SQLite database for future reference.

---

## Features

- **RabbitMQ Integration**: Consumes messages from a RabbitMQ queue.
- **Email Notifications**: Sends emails to patients and doctors based on the message content.
- **Database Storage**: Stores notifications in a SQLite database for logging and retrieval.
- **Swagger Documentation**: Provides API documentation for the Flask-based notification service.
- **Environment Variables**: Uses `.env` for secure configuration of sensitive data.

---

## Technologies Used

- **Python**: Primary programming language.
- **Flask**: Web framework for the notification service.
- **SQLAlchemy**: ORM for database interactions.
- **RabbitMQ**: Message broker for handling notifications.
- **SMTP (Gmail)**: For sending email notifications.
- **Swagger**: API documentation.
- **SQLite**: Lightweight database for storing notifications.

---

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.8+**
- **RabbitMQ**
- **Gmail Account** (for sending emails) or another SMTP service.

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/medi-connect-notifications.git
   cd medi-connect-notifications
