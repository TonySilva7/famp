from pytz import timezone
from typing import Optional, List
from datetime import datetime, timedelta
from pydantic import EmailStr

from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import UserModel
from core.configs import settings
from core.security import verify_password

# Permite a criação de um endpoint de autenticação
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/users/login",
)


async def authenticate_user(email: EmailStr, password: str, db: AsyncSession) -> Optional[UserModel]:
    async with db as session:
        query = select(UserModel).filter(UserModel.email == email)
        result = await session.execute(query)
        user: UserModel = result.scalars().unique().one_or_none()

        if not user:
            return None

        if not verify_password(password, user.password):
            return None

        return user


def _create_token(type_token: str, ttl: timedelta, subject: str) -> str:
    # Saiba mais sobre o padrão de payload em: http://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    payload = {}

    sp = timezone("America/Sao_Paulo")
    expires = datetime.now(tz=sp) + ttl

    payload["type"] = type_token
    payload["exp"] = expires
    payload["iat"] = datetime.now(tz=sp)  # Issued at time | Gerado em data e hora atual
    payload["sub"] = str(subject)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.ALGORITHM)


def create_access_token(sub: str) -> str:
    token = _create_token(
        type_token="access_token",
        ttl=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        subject=sub,
    )
    print("MY_TOKEN: ", token)
    return token
