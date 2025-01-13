from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User

async def get_user(db: AsyncSession, email: str):
    query = select(User).where(User.email == str(email))
    result = await db.execute(query)
    user = result.first()
    # (user,)
    return user[0]

# If you need to get all users
async def get_all_users(db: AsyncSession):
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all()
    return users

# For inserting
async def create_user(db: AsyncSession, user_data: dict):
    user = User(**user_data)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

# For updating
async def update_user(db: AsyncSession, user: User, user_data: dict):
    for key, value in user_data.items():
        setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user

# For deleting
async def delete_user(db: AsyncSession, user: User):
    await db.delete(user)
    await db.commit()
