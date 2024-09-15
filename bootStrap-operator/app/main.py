from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from app.routers import node
from app.database import Base, engine, get_db
from app.services import get_all_nodes

app = FastAPI()

# CORS setup to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers, including Authorization
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(node.router)

# List of required services
REQUIRED_SERVICES = ["load_balancer", "frontend", "api"]


def check_services_and_get_lb_url(db: Session):
    """Check if all required services are up and return the Load Balancer URL if available."""
    try:
        # Fetch all nodes using the existing get_all_nodes function from services.py
        registered_nodes = get_all_nodes(db)

        # Check for required services and find the load balancer details
        running_services = {node.service_type for node in registered_nodes}
        lb_node = next(
            (node for node in registered_nodes if node.service_type == "frontend"), None
        )

        # If any required service is missing or the load balancer is not found, return False and None
        if (
            not all(service in running_services for service in REQUIRED_SERVICES)
            or lb_node is None
        ):
            return False, None

        # Construct the Load Balancer URL from its IP and port
        lb_url = f"http://{lb_node.ip_address}:{lb_node.port}"
        return True, lb_url

    except Exception as e:
        print(f"Error checking services: {e}")
        return False, None


@app.get("/", response_class=HTMLResponse)
async def index(db: Session = Depends(get_db)):
    # Check if all services are running and get Load Balancer URL
    services_ready, lb_url = check_services_and_get_lb_url(db)

    if services_ready and lb_url:
        # If all services are available, redirect to the load balancer
        return RedirectResponse(lb_url)
    else:
        # Show a "Please wait" holding page and auto-refresh to check again
        return HTMLResponse(
            """
        <html>
            <head>
                <title>Loading...</title>
                <meta http-equiv="refresh" content="5">  <!-- Auto-refresh every 5 seconds -->
            </head>
            <body>
                <h1>Services are starting up, please wait...</h1>
                <p>We are waiting for all required services to be available. This page will refresh automatically.</p>
            </body>
        </html>
        """
        )
