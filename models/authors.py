from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Author(BaseModel):
    id_author: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del autor"
        )
    
    first_name: Optional[str] = Field(
        default=None,
        description="El nombre del autor",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["Oscar","Luis"]
    )

    last_name: Optional[str] = Field(
        default=None,
        description="El apellido del autor",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["García","Martínez"]
    )