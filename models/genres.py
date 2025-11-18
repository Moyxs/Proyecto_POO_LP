from pydantic import BaseModel, Field
from typing import Optional
import re

class Genres(BaseModel):
    id_genres: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del género del libro"
        )
    
    name_genres: Optional[str] = Field(
        default=None,
        description="El nombre del género del libro",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["Ficción","Aventura"]
    )

    description: Optional[str] = Field(
        default=None,
        description="La descripción del género del libro",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["Género literario que incluye obras imaginativas","Género literario basado en hechos reales"]
    )