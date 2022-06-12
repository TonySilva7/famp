from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, status, Path
from models import Curso, cursos

app = FastAPI(
    title="Cursos API",
    description="API para acesso aos cursos",
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
)


@app.get(
    "/cursos",
    status_code=status.HTTP_200_OK,
    description="Retorna uma lista de cursos",
    summary="Lista os cursos",
    response_model=Dict[str, List[Curso]],
    response_description="Lista de cursos encontrados",
)
async def get_cursos():
    return {"cursos": cursos}


@app.get("/cursos/{id}", status_code=status.HTTP_200_OK)
async def get_curso(id: int = Path(default=None, title="ID do curso", description="Range de 1 a 3", gt=0, lt=4)):
    try:
        curso = cursos[id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")


@app.post("/cursos", status_code=status.HTTP_201_CREATED, response_model=Dict[str, Curso])
async def post_curso(curso: Curso):
    next_id: int = len(cursos) + 1

    if next_id in cursos:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Curso já existe")

    curso.id = next_id
    cursos.append(curso.dict())
    return {"curso": curso}


@app.put("/cursos/{id}", status_code=status.HTTP_200_OK, response_model=Dict[str, Curso])
async def put_curso(id: int, curso: Curso):

    for i in range(len(cursos)):
        c = dict(cursos[i])

        if c.get("id") == id:
            curso.id = id
            cursos[i] = curso.dict()
            return {"curso": curso}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")


@app.delete("/cursos/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(id: int):
    if id not in cursos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

    del cursos[id]


# Entry point of the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True, debug=True)
