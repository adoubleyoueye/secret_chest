from typing import Optional
import uuid
from pydantic import BaseModel, Field


class MessageModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Pineapples don't belong on pizza.",
            }
        }