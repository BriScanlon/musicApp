from fastapi import FastAPI
from app.routers import node
from app.database import Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(node.router)

@app.get("/")
def read_root():
    return {"message": "Bootstrap Operator is running"}
