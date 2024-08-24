from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import register_node, deregister_node, get_node_by_service, update_heartbeat
from pydantic import BaseModel

router = APIRouter()

class NodeRegistration(BaseModel):
    service_type: str
    ip_address: str
    port: int

class HeartbeatUpdate(BaseModel):
    node_id: int

@router.post("/register")
def register(node: NodeRegistration, db: Session = Depends(get_db)):
    db_node = register_node(db, node.service_type, node.ip_address, node.port)
    return {"node_id": db_node.id, "message": "Node registered successfully"}

@router.get("/lookup/{service_type}")
def lookup(service_type: str, db: Session = Depends(get_db)):
    node = get_node_by_service(db, service_type)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"ip_address": node.ip_address, "port": node.port}

@router.delete("/deregister/{node_id}")
def deregister(node_id: int, db: Session = Depends(get_db)):
    success = deregister_node(db, node_id)
    if not success:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"message": "Node deregistered successfully"}

@router.post("/heartbeat")
def heartbeat(heartbeat_data: HeartbeatUpdate, db: Session = Depends(get_db)):
    node = update_heartbeat(db, heartbeat_data.node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"message": "Heartbeat updated", "last_heartbeat": node.last_heartbeat}
