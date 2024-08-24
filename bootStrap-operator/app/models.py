from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Node(Base):
    __tablename__ = "nodes"

    id = Column(Integer, primary_key=True, index=True)
    service_type = Column(String(50), index=True)
    ip_address = Column(String(50))
    port = Column(Integer)
    last_heartbeat = Column(DateTime, default=datetime.utcnow)

