from typing import Optional
from pydantic import BaseModel


from typing import Optional
from pydantic import BaseModel


class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: str
    horas: int
