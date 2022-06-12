from typing import List, Optional
from pydantic import BaseModel


from typing import Optional
from pydantic import BaseModel


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: str
    horas: int


curso1 = Curso(id=1, titulo="Python", aulas="Aula de Python", horas=4)
curso2 = Curso(id=2, titulo="Java", aulas="Aula de Java", horas=4)
curso3 = Curso(id=3, titulo="C#", aulas="Aula de C#", horas=4)

cursos: List[Curso] = [
    curso1,
    curso2,
    curso3,
]
