from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Gender(BaseModel):
    id_gender: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del género"
        )
    
    name_geder: Optional[str] = Field(
        default=None,
        description="El nombre del género",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["Ficción","No Ficción"]
    )

    description: Optional[str] = Field(
        default=None,
        description="La descripción del género",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["Género literario que incluye obras imaginativas","Género literario basado en hechos reales"]
    )