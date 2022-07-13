from typing import List, Optional, Any
from fastapi import APIRouter, HTTPException, Depends, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.user_model import UserModel
from schemas.user_achema import UserSchemaBase, UserSchemaCreate, UserSchemaUpdate, UserSchemaArticles
from core.deps import get_session, get_current_user
from core.security import generate_password_hash
from core.auth import authenticate_user, create_access_token

router = APIRouter()

# get user logged in
@router.get("/logged", response_model=UserSchemaBase)
def get_logged_user(user_logged: UserModel = Depends(get_current_user)):
    return user_logged


# POST / Sign up
@router.post("/signup", response_model=UserSchemaBase, status_code=status.HTTP_201_CREATED)
async def signup(user: UserSchemaCreate, db: AsyncSession = Depends(get_session)):

    async with db as session:
        try:
            new_user = UserModel(
                name=user.name,
                last_name=user.last_name,
                email=user.email,
                password=generate_password_hash(user.password),
                is_admin=user.is_admin,
            )

            session.add(new_user)
            await session.commit()
            return new_user
        except Exception as e:
            print("MEU_ERRO: ", e)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


# get all users
@router.get("/", response_model=List[UserSchemaBase])
async def get_users(db: AsyncSession = Depends(get_session)):
    try:
        async with db as session:
            query = select(UserModel)
            result = await session.execute(query)
            users: List[UserSchemaBase] = result.scalars().unique().all()
            return users

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)


# get user by id
@router.get("/{user_id}", response_model=UserSchemaArticles, status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user


# update user
@router.put("/{user_id}", response_model=UserSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def update_user(user_id: int, user: UserSchemaUpdate, db: AsyncSession = Depends(get_session)):

    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_db: UserSchemaBase = result.scalars().unique().one_or_none()

        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        user_db.name = user.name if user.name else user_db.name
        user_db.last_name = user.last_name if user.last_name else user_db.last_name
        user_db.email = user.email if user.email else user_db.email
        user_db.password = user.password if generate_password_hash(user.password) else user_db.password
        user_db.is_admin = user.is_admin if user.is_admin else user_db.is_admin

        await session.commit()
        return user_db


# delete user
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UserModel).filter(UserModel.id == user_id)
        result = await session.execute(query)
        user_db: UserSchemaArticles = result.scalars().unique().one_or_none()

        if user_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        await session.delete(user_db)
        await session.commit()

        return Response(status=status.HTTP_204_NO_CONTENT)


# login - POST
@router.post("/login", response_model=UserSchemaBase, status_code=status.HTTP_200_OK)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    user = await authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")

    token = create_access_token(sub=user.id)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": token, "token_type": "bearer"})
