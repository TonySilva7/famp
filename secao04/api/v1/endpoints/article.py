from typing import List
from fastapi import APIRouter, HTTPException, Depends, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.article_model import ArticleModel
from models.user_model import UserModel
from schemas.article_schema import ArticleSchema
from core.deps import get_session, get_current_user


router = APIRouter()

# POST article
@router.post("/ ", response_model=ArticleSchema, status_code=status.HTTP_201_CREATED)
async def create_article(
    article: ArticleSchema,
    user_logged: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> ArticleSchema:

    new_article: ArticleModel = ArticleModel(
        title=article.title,
        description=article.description,
        url_font=article.url_font,
        user_id=user_logged.id,
    )

    db.add(new_article)
    await db.commit()
    db.refresh(new_article)

    return new_article


# GET articles (usuário não precisa estar logado)
@router.get("/", response_model=List[ArticleSchema])
async def get_articles(db: AsyncSession = Depends(get_session)) -> List[ArticleSchema]:
    with db as session:
        query = select(ArticleModel)
        result = await session.execute(query)
        articles: List[ArticleModel] = result.scalars().unique().all()

        return articles


# GET article by id
@router.get("/{id}", response_model=ArticleSchema, status_code=status.HTTP_200_OK)
async def get_article_by_id(
    id: int,
    db: AsyncSession = Depends(get_session),
) -> ArticleSchema:
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == id)
        result = await session.execute(query)
        article: ArticleModel = result.scalars().unique().one_or_none()

        if not article:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

        return article


# PUT article
@router.put("/{id}", response_model=ArticleSchema, status_code=status.HTTP_202_ACCEPTED)
async def update_article(
    id: int,
    article: ArticleSchema,
    user_logged: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> ArticleSchema:
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == id)
        result = await session.execute(query)
        article_db: ArticleModel = result.scalars().unique().one_or_none()

        if not article_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

        if article_db.user_id != user_logged.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to update this article"
            )

        article_db.title = article.title if article.title else article_db.title
        article_db.description = article.description if article.description else article_db.description
        article_db.url_font = article.url_font if article.url_font else article_db.url_font
        article_db.user_id = user_logged.id if user_logged.id != article_db.user_id else article_db.user_id

        await session.commit()
        session.refresh(article_db)

        return article_db


# DELETE article
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    id: int,
    user_logged: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_session),
) -> Response:
    async with db as session:
        query = select(ArticleModel).filter(ArticleModel.id == id).filter(ArticleModel.user_id == user_logged.id)
        result = await session.execute(query)
        article_db: ArticleModel = result.scalars().unique().one_or_none()

        if not article_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")

        if article_db.user_id != user_logged.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="You don't have permission to delete this article"
            )

        await session.delete(article_db)
        await session.commit()

        return Response(status=status.HTTP_204_NO_CONTENT)
