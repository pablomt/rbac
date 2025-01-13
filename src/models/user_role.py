from sqlalchemy import Column, TIMESTAMP, text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))