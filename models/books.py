from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
import re

class Books(BaseModel):
    id: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del libro"
        )
    
    id_genre: Optional[int] = Field(
        default=None,
        description="El ID del género del libro"
    )

    title: Optional[str] = Field(
        default=None,
        description="El título del libro",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["El Quijote","Cien Años de Soledad"]
    )

    isbn: Optional[str] = Field(
        default=None,
        description="El ISBN del libro",
        pattern=r"^(97(8|9))?[- ]?\d{1,5}[- ]?\d{1,7}[- ]?\d{1,7}[- ]?(\d|X)$",
        examples=["978-3-16-148410-0","0-306-40615-2"]
    )
    date_published: Optional[date] = Field(
        default=None,
        description="La fecha de publicación del libro",
        examples=["2023-10-15","2000-01-01"]
    )

    its_active: Optional[bool] = Field(
        default=None,
        description="Indica si el libro está en existencia o no",
        examples=[True, False]
    )

