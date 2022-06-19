from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import Session


async def get_session() -> Generator:
    session: AsyncSession = Session

    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
