# run.py

import os
import logging
from config import settings
from app.initialize_db import initialize_database

import uvicorn

# Import the app from main.py
from app.main import app

# Create logs directory if it doesn't exist
if not os.path.exists('logs'):
    os.makedirs('logs')

# Convert LOG_LEVEL to uppercase and get logging level
numeric_log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

# Setup logging
logging.basicConfig(
    level=numeric_log_level,
    format=settings.LOG_FORMAT,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/app.log", encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Run the application using Uvicorn
def start_app():
    try:
        logger.info("Starting the eZzDay Waste Management System...")
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=settings.DEBUG,  # Assuming DEBUG is a boolean
            log_level=settings.LOG_LEVEL.lower(),
            workers=1  # Adjust as needed
        )
    except Exception as e:
        logger.error(f"Failed to start application: {e}")


if __name__ == "__main__":
    # Prevent database initialization in Uvicorn's reloader child process
    if os.environ.get("RUN_MAIN") != "true":
        initialize_database()
    start_app()