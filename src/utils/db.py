from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from src.models.user import User
from src.models.role import Role
from src.models.user_role import UserRole
from src.models.permission import Permission
from src.models.role_permission import RolePermission
from src.models.audit_log import AuditLog

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from src.config import settings

class Base(DeclarativeBase):
    pass

# Create async engine
engine = None
async_session_maker = None

async def init_db():
    global engine, async_session_maker

    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
    )

    async_session_maker = async_sessionmaker(
        engine,
        expire_on_commit=False,
        autocommit=False,
        autoflush=False,
    )

async def close_db():
    global engine
    if engine:
        await engine.dispose()


# Database dependency
async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()