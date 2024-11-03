# settings.py

from starlette.config import Config
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()
config = Config(".env")

# General Configurations
DEBUG = config("DEBUG", cast=bool, default=False)
SECRET_KEY = config("SECRET_KEY", cast=str)
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is not set in the environment variables or .env file.")
APP_NAME = config("APP_NAME", cast=str, default="eZzDay Waste Management System")

# Database Configuration
DATABASE_URL = config("DATABASE_URL", cast=str)
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set in the environment variables or .env file.")

# Logging Configuration
LOG_LEVEL = config("LOG_LEVEL", cast=str, default="INFO")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_FILE = config("LOG_FILE", cast=str, default="logs/app.log")

# Email Configuration (for sending notifications)
SMTP_SERVER = config("SMTP_SERVER", cast=str)
SMTP_PORT = config("SMTP_PORT", cast=int, default=587)
EMAIL_USERNAME = config("EMAIL_USERNAME", cast=str)
EMAIL_PASSWORD = config("EMAIL_PASSWORD", cast=str)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)

# CORS Configuration
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=str,
    default="http://localhost,https://mytrustedfrontend.com"
).split(",")

# JWT Configurations
JWT_SECRET = config("JWT_SECRET", cast=str)
if not JWT_SECRET:
    raise ValueError("JWT_SECRET is not set in the environment variables or .env file.")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = config("JWT_EXPIRATION_HOURS", cast=int, default=1)

# Security Enhancements
CONTENT_SECURITY_POLICY = config(
    "CONTENT_SECURITY_POLICY",
    cast=str,
    default="default-src 'self'; script-src 'self'"
)

# Session Configuration
SESSION_COOKIE = config("SESSION_COOKIE", cast=str, default="ezzday_session")
SESSION_COOKIE_AGE = config("SESSION_COOKIE_AGE", cast=int, default=3600)