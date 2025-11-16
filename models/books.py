from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Books(BaseModel):
    id_book: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del libro"
        )
    
    id_genre: Optional[int] = Field(
        default=None,
        description="El ID del género del libro",
        pattern=r"^[A-Za-z0-9'-]+$",
    )

    title: Optional[str] = Field(
        default=None,
        description="El título del libro",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["El Quijote","Cien Años de Soledad"]
    )

