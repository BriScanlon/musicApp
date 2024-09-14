from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.services import (
    register_node,
    deregister_node,
    get_node_by_service,
    update_heartbeat,
    get_all_nodes,
)
from pydantic import BaseModel

router = APIRouter()


class NodeRegistration(BaseModel):
    service_type: str
    ip_address: str
    port: int


class HeartbeatUpdate(BaseModel):
    node_id: int


@router.post("/api/node/register")
def register(node: NodeRegistration, db: Session = Depends(get_db)):
    db_node = register_node(db, node.service_type, node.ip_address, node.port)
    return {"node_id": db_node.id, "message": "Node registered successfully"}


@router.post("/api/node/heartbeat")
def heartbeat(heartbeat_data: HeartbeatUpdate, db: Session = Depends(get_db)):
    node = update_heartbeat(db, heartbeat_data.node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"message": "Heartbeat updated", "last_heartbeat": node.last_heartbeat}


@router.get("/api/node/lookup/{service_type}")
def lookup(service_type: str, db: Session = Depends(get_db)):
    # Get all nodes with the matching service_type
    nodes = get_node_by_service(db, service_type)

    # If no nodes are found, raise an HTTPException
    if not nodes:
        raise HTTPException(status_code=404, detail="No nodes found")

    # Return a list of node IP addresses and ports
    return [{"ip_address": node.ip_address, "port": node.port} for node in nodes]


@router.get("/api/nodes")
def list_all_nodes(db: Session = Depends(get_db)):
    nodes = get_all_nodes(db)

    if not nodes:
        raise HTTPException(status_code=404, detail="No nodes registered.")

    # Return all node details as a list of dictionaries
    return [
        {
            "id": node.id,
            "service_type": node.service_type,
            "ip_address": node.ip_address,
            "port": node.port,
            "last_heartbeat": node.last_heartbeat,
        }
        for node in nodes
    ]


@router.delete("/api/node/deregister/{node_id}")
def deregister(node_id: int, db: Session = Depends(get_db)):
    success = deregister_node(db, node_id)
    if not success:
        raise HTTPException(status_code=404, detail="Node not found")
    return {"message": "Node deregistered successfully"}
