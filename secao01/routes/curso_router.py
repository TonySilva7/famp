from typing import Dict, List
from fastapi import APIRouter, HTTPException, Path, status

from models import Curso, cursos

router = APIRouter()


@router.get(
    "/cursos",
    status_code=status.HTTP_200_OK,
    description="Retorna uma lista de cursos",
    summary="Lista os cursos",
    response_model=Dict[str, List[Curso]],
    response_description="Lista de cursos encontrados",
)
async def get_cursos():
    return {"cursos": cursos}


@router.get("/cursos/{id}", status_code=status.HTTP_200_OK)
async def get_curso(id: int = Path(default=None, title="ID do curso", description="Range de 1 a 3", gt=0, lt=4)):

    curso = await find_curso(id)
    return curso


@router.post("/cursos", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Curso])
async def post_curso(curso: Curso):
    next_id: int = len(cursos) + 1

    has_course: bool = await find_curso(next_id)

    if has_course:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Curso já existe")

    curso.id = next_id
    cursos.append(curso.dict())
    return {"curso": curso}


@router.put("/cursos/{id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Curso])
async def put_curso(id: int, curso: Curso):
    course: Curso = await find_curso(id)

    if course is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    index = cursos.index(course)

    curso.id = id
    course = curso.dict()
    cursos[index] = course

    return {"curso": course}


@router.delete("/cursos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id: int):
    if id not in cursos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    del cursos[id]


async def find_curso(id: int) -> bool:
    for i in range(len(cursos)):
        c = dict(cursos[i])

        if c.get("id") == id:
            return c
    return None
