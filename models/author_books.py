from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date

class Author_book(BaseModel):

    id_book: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del libro"
    )
    
    id_author: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del libro"
    )