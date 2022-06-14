from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import Session


async def get_session() -> Generator:
    """
    Obtém uma nova seção com banco de dados.
    """
    session: AsyncSession = Session()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()

    return session
