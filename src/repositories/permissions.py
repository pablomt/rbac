from typing import List
from sqlalchemy import select
from src.models.permission import Permission
from sqlalchemy.ext.asyncio import AsyncSession
import uuid


async def get_permisions(db: AsyncSession, permision_ids: List[uuid.UUID]):
    query = select(Permission).where(Permission.id.in_(permision_ids))
    result = await db.execute(query)
    permissions = result.all()
    return permissions