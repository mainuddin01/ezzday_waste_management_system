# app/initialize_db.py

import logging
from app.database import db
from app.components.auth.models import User
from app.components.client.models import Client
from app.components.fleet.models import Truck
from app.components.zone.models import Zone
from app.components.route.models import Route
from app.components.crew.models import Crew
from app.components.driver.models import Driver
from app.components.loader.models import Loader
from app.components.assignment.models import Assignment
from app.components.schedule.models import Schedule
from app.components.event.models import Event
from app.components.issues.models import Issue
from app.components.report.models import Report

logger = logging.getLogger(__name__)

def initialize_database():
    """
    Initializes the database by creating all necessary tables.
    """
    try:
        logger.info("Starting database initialization...")
        
        # List of all model classes to create tables for
        models = [
            User,
            Client,
            Truck,
            Zone,
            Route,
            Crew,
            Driver,
            Loader,
            Assignment,
            Schedule,
            Event,
            Issue,
            Report
        ]

        # Create tables for each model
        for model in models:
            model.create_table()
            logger.debug(f"Ensured table for model '{model.__name__}' exists.")

        # Create admin user if it doesn't exist
        create_admin_user()

        logger.info("Database initialization complete.")
    except Exception as e:
        logger.exception("Error during database initialization.")
        raise

def create_admin_user():
    """Creates a default admin user if it doesn't already exist."""
    admin_username = 'admin'
    admin_password = 'admin'
    admin_role = 'Admin'  # Ensure consistent role naming

    if not User.find_by_username(admin_username):
        admin_user = User(username=admin_username, role=admin_role)
        admin_user.set_password(admin_password)
        admin_user.save()
        logger.info("Admin user created.")
    else:
        logger.info("Admin user already exists.")

if __name__ == "__main__":
    initialize_database()