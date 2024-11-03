# app/main.py

import logging
from dotenv import load_dotenv
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from fasthtml.common import *
from tilted import *
from app.components.auth.routes import setup_routes as setup_auth_routes
from app.components.assignment.routes import setup_routes as setup_assignment_routes
from app.components.crew.routes import setup_routes as setup_crew_routes
from app.components.client.routes import setup_routes as setup_client_routes
from app.components.driver.routes import setup_routes as setup_driver_routes
from app.components.event.routes import setup_routes as setup_event_routes
from app.components.fleet.routes import setup_routes as setup_fleet_routes
from app.components.issues.routes import setup_routes as setup_issues_routes
from app.components.loader.routes import setup_routes as setup_loader_routes
from app.components.report.routes import setup_routes as setup_report_routes
from app.components.route.routes import setup_routes as setup_route_routes
from app.components.schedule.routes import setup_routes as setup_schedule_routes
from app.components.zone.routes import setup_routes as setup_zone_routes

from config.settings import SECRET_KEY, DEBUG, SESSION_COOKIE, CORS_ALLOWED_ORIGINS
from app.utils.helpers.helpers import setup_logging, SecurityHeadersMiddleware

# Load environment variables from .env file
load_dotenv()

# Setup logging
logger = setup_logging()

# Initialize FastHTML application with middleware
middleware = [
    Middleware(SessionMiddleware, secret_key=SECRET_KEY, session_cookie=SESSION_COOKIE),
    Middleware(SecurityHeadersMiddleware),
    Middleware(
        CORSMiddleware,
        allow_origins=CORS_ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]

# Link the Pico CSS
headers = [
    Link(rel="stylesheet", href="/static/css/pico.min.css", type="text/css")
]

app = FastHTML(middleware=middleware, hdrs=headers)

# Mount static files directory to serve CSS and other static assets
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Setup application routes for each component
setup_auth_routes(app)
setup_assignment_routes(app)
setup_crew_routes(app)
setup_client_routes(app)
setup_driver_routes(app)
setup_event_routes(app)
setup_fleet_routes(app)
setup_issues_routes(app)
setup_loader_routes(app)
setup_report_routes(app)
setup_route_routes(app)
setup_schedule_routes(app)
setup_zone_routes(app)

# Add a route for favicon.ico
@app.get("/favicon.ico")
async def favicon():
    return FileResponse("app/static/assets/favicon.ico")

logger.info("All routes successfully registered.")