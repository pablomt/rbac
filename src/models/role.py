from sqlalchemy import Column, String, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class Role(Base):
    __tablename__ = "roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    description = Column(String)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))