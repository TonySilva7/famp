from typing import Optional, List
from pydantic import BaseModel, EmailStr, BaseModelEncoder, HttpUrl
from schemas.article_schema import ArticleSchema


# Usado para devolver um usuário
class UserSchemaBase(BaseModel):
    id: Optional[int] = None
    name: str
    last_name: str
    email: EmailStr
    is_admin: bool = False

    class Config:
        orm_mode = True
        # allow_population_by_field_name = True
        # validate_all = True
        # extra = "forbid"
        # allow_mutation = False
        # json_encoders = {
        #     BaseModel: BaseModelEncoder,
        #     HttpUrl: lambda url: url.__str__(),
        # }


# será usado para criar o usuário
class UserSchemaCreate(UserSchemaBase):
    password: str


class UserSchemaArticles(UserSchemaBase):
    articles: List[ArticleSchema] = []


class UserSchemaUpdate(UserSchemaBase):
    name = Optional[str]
    last_name = Optional[str]
    email = Optional[str]
    password = Optional[str]
    is_admin = Optional[bool]
