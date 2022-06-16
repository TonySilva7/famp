from turtle import title
from typing import List
from unittest import result

from fastapi import APIRouter
from fastapi import status
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.course_model import CourseModel
from schemas.course_schema import CourseSchema
from core.deps import get_session


router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CourseSchema)
async def create_course(course: CourseSchema, db: AsyncSession = Depends(get_session)):
    try:
        new_course = CourseModel(title=course.title, lesson=course.lesson, hours=course.hours)
        db.add(new_course)
        await db.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível criar o curso."
        )

    return new_course


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[CourseSchema])
async def get_courses(db: AsyncSession = Depends(get_session)):
    try:
        async with db as session:
            query = select(CourseModel)
            result = await session.execute(query)
            cursos: List[CourseModel] = result.scalars().all()

            return cursos
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível obter os cursos."
        )


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=CourseSchema)
async def get_course(id: int, db: AsyncSession = Depends(get_session)):
    try:
        async with db as session:
            query = select(CourseModel).filter(CourseModel.id == id)
            result = await session.execute(query)
            course: CourseModel = result.scalars_one_or_none()

            if course is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado."
                )

            return course
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível obter o curso."
        )


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED, response_model=CourseSchema)
async def update_course(id: int, course: CourseSchema, db: AsyncSession = Depends(get_session)):
    try:
        async with db as session:
            query = select(CourseModel).filter(CourseModel.id == id)
            result = await session.execute(query)
            course_old: CourseModel = result.scalars_one_or_none()

            if course_old is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado."
                )

            course_old.title = course.title
            course_old.lesson = course.lesson
            course_old.hours = course.hours

            await session.commit()

            return course_old
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível atualizar o curso."
        )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(id: int, db: AsyncSession = Depends(get_session)):
    try:
        async with db as session:
            query = select(CourseModel).filter(CourseModel.id == id)
            result = await session.execute(query)
            course: CourseModel = result.scalars_one_or_none()

            if course is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado."
                )

            await session.delete(course)
            await session.commit()

            return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Não foi possível deletar o curso."
        )
