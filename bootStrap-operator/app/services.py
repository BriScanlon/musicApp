from sqlalchemy.orm import Session
from app.models import Node
from datetime import datetime

def register_node(db: Session, service_type: str, ip_address: str, port: int):
    node = Node(service_type=service_type, ip_address=ip_address, port=port)
    db.add(node)
    db.commit()
    db.refresh(node)
    return node

def deregister_node(db: Session, node_id: int):
    node = db.query(Node).filter(Node.id == node_id).first()
    if node:
        db.delete(node)
        db.commit()
        return True
    return False

def get_node_by_service(db: Session, service_type: str):
    node = db.query(Node).filter(Node.service_type == service_type).first()
    return node

def update_heartbeat(db: Session, node_id: int):
    node = db.query(Node).filter(Node.id == node_id).first()
    if node:
        node.last_heartbeat = datetime.utcnow()
        db.commit()
        db.refresh(node)
        return node
    return None
