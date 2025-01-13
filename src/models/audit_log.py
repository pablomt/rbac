from sqlalchemy import Column, String, Boolean, TIMESTAMP, text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action_type = Column(String, nullable=False)  # Acción: 'READ', 'WRITE', 'DELETE'
    resource = Column(String, nullable=False)  # Recurso (ej.: 'S3://my-bucket/delta-table')
    granted = Column(Boolean, nullable=False)
    details = Column(String)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))