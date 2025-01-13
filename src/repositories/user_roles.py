from sqlalchemy import select
from src.models.user_role import UserRole
from sqlalchemy.ext.asyncio import AsyncSession
import uuid


async def get_user_roles(db: AsyncSession, user_id: uuid.UUID):
    query = select(UserRole).where(UserRole.user_id == user_id)
    result = await db.execute(query)
    user_roles = result.all()
    return user_roles