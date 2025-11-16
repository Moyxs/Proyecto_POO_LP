from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class Book_author(BaseModel):

    id_book: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del libro"
    )
    
    id_author: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del libro"
    )

    date_published: Optional[date] = Field(
        default=None,
        description="La fecha de publicación del libro por el autor",
        examples=["2023-10-15","2000-01-01"]
    )