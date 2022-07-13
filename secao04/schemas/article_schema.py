from typing import Optional
from pydantic import BaseModel, HttpUrl


class ArticleSchema(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    url_font: HttpUrl
    user_id: Optional[int]

    class Config:
        orm_mode = True
        # allow_population_by_field_name = True
        # validate_all = True
        # extra = "forbid"
        # allow_mutation = False
        # json_encoders = {
        #     pydantic.BaseModel: pydantic.BaseModelEncoder,
        #     HttpUrl: lambda url: url.__str__(),
        # }
