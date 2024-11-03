# helpers.py

import re
import logging
from datetime import datetime
from starlette.websockets import WebSocket
from starlette.middleware.base import BaseHTTPMiddleware

# Configure Logging
def setup_logging():
    """Sets up logging for the application with a standard format."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler("logs/app.log", encoding='utf-8')
        ]
    )
    logger = logging.getLogger(__name__)
    return logger

logger = setup_logging()

# Helper Functions

# Date Formatting
def format_date(date):
    """Formats a date into YYYY-MM-DD format."""
    if isinstance(date, datetime):
        return date.strftime("%Y-%m-%d")
    else:
        raise ValueError("Expected a datetime object.")

# Email Validation
def validate_email(email):
    """Validates the given email address format."""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        logger.warning(f"Invalid email format: {email}")
        return False
    return True

# Phone Number Validation
def validate_phone_number(phone_number):
    """Validates a phone number to ensure it contains only digits and has a valid length."""
    pattern = r"^\d{10,15}$"
    if not re.match(pattern, phone_number):
        logger.warning(f"Invalid phone number format: {phone_number}")
        return False
    return True

# Date Format Validation
def validate_date_format(date_string, format="%Y-%m-%d"):
    """Validates if the input string matches the date format."""
    try:
        datetime.strptime(date_string, format)
        return True
    except ValueError:
        logger.error(f"Invalid date format: {date_string}. Expected format: {format}.")
        return False

# WebSocket Utilities
async def send_real_time_update(websocket: WebSocket, message: str):
    """Sends a real-time update message over the given WebSocket connection."""
    await websocket.accept()
    try:
        await websocket.send_text(message)
        logger.info(f"WebSocket message sent: {message}")
    except Exception as e:
        logger.error(f"Error while sending WebSocket message: {str(e)}")
    finally:
        await websocket.close()

async def receive_real_time_data(websocket: WebSocket):
    """Receives data in real-time through WebSocket."""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Data received via WebSocket: {data}")
            # Handle the received data here as per your business logic
    except Exception as e:
        logger.error(f"Error while receiving WebSocket data: {str(e)}")
    finally:
        await websocket.close()

# Security Enhancements
def sanitize_input(input_string):
    """Sanitizes user input to avoid SQL injection and XSS attacks."""
    sanitized_string = re.sub(r"[\'\";--]", "", input_string)  # Remove dangerous characters
    logger.debug(f"Sanitized input: {sanitized_string}")
    return sanitized_string

def enforce_secure_headers(response):
    """Adds secure headers to the response object to enhance security."""
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    logger.info("Secure headers added to response.")
    return response

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware to enforce security headers on all responses."""
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response = enforce_secure_headers(response)
        return response

# CORS Setup
def setup_cors(app, origins):
    """Adds CORS middleware to allow cross-origin requests from trusted domains."""
    from starlette.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS middleware setup complete.")