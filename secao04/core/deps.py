from typing import Generator, Optional
from fastapi import Depends, HTTPException, status

from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from core.db import Session
from core.auth import oauth2_scheme
from core.configs import settings
from models.user_model import UserModel


class TokenData(BaseModel):
    username: Optional[str] = None


# create function to get session
async def get_session() -> Generator:
    session: AsyncSession = Session()

    try:
        yield session
    except Exception as e:
        print(e)
        session.close()
        raise e
    finally:
        session.close()
        print("Session closed")


async def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> Optional[UserModel]:

    credential_exeption: HTTPException = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")  # 'sub' é o id do usuário

        if username is None:
            raise credential_exeption

        token_data: TokenData = TokenData(username=username)
    except JWTError:
        raise credential_exeption
    except Exception as e:
        print(e)
        return None

    async with db as session:
        query = select(UserModel).filter(UserModel.id == int(token_data.username))
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if user is None:
            raise credential_exeption

        return user
