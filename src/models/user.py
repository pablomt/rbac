from sqlalchemy import Column, String, Integer, ForeignKey, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False) # Cognito user
    name = Column(String, nullable=False)
    first_last_name = Column(String, nullable=False)
    second_last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone_number = Column(Integer, nullable=False)
    #role_id = Column(UUID(as_uuid=True), ForeignKey("roles.id"))
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    updated_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))
    updated_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

