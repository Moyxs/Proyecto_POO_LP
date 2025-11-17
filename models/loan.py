from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import date
import re

class Loan(BaseModel):
    id_Loan: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del préstamo"
        )
    
    id_customer: Optional[int] = Field(
        default=None,
        description="El ID del cliente que realiza el préstamo",
    )

    date_loan: Optional[date] = Field(
        default=None,
        description="La fecha en que se realiza el préstamo",
        examples=["2023-10-15","2022-05-20"]
    )

    date_devolution: Optional[date] = Field(
        default=None,
        description="La fecha en que se devuelve el libro",
        examples=["2023-11-15","2022-06-20"]
    )

    loan_active: Optional[bool] = Field(
        default=True,
        description="El estado del préstamo",
        pattern=r"^(activo|devuelto|retrasado)$",
        examples=["activo","devuelto"]
    )