from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Customer(BaseModel):
    id_author: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del cliente"
        )
    
    first_name: Optional[str] = Field(
        default=None,
        description="El nombre del cliente",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["Oscar","Luis"]
    )

    last_name: Optional[str] = Field(
        default=None,
        description="El apellido del cliente",
        pattern=r"^[A-Za-zÀ-ÖØ-öø-ÿ\s'-]+$",
        examples=["García","Martínez"]
    )

    age: Optional[int] = Field(
        default=None,
        description="La edad del cliente",
        ge=14
    )
    email: Optional[str] = Field(
        default=None,
        description="El correo electrónico del cliente",
        pattern=r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        examples=["usuario@example.com"]
    )