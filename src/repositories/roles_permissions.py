from typing import List
from sqlalchemy import select
from src.models.role_permission import RolePermission
from sqlalchemy.ext.asyncio import AsyncSession
import uuid


async def get_roles_permisions(db: AsyncSession, roles_ids: List[uuid.UUID]):
    query = select(RolePermission).where(RolePermission.role_id.in_(roles_ids))
    result = await db.execute(query)
    roles_permissions = result.all()
    return roles_permissions