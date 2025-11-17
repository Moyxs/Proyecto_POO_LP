from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

class Loan_Books(BaseModel):

    id_book: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del libro"
    )
    
    id_loan: Optional[int] = Field(
        default=None,
        description="El ID autoincrementable del préstamo"
    )

    return_status: Optional[bool] = Field(
        default=False,
        description="Indica si el libro ha sido devuelto o no",
    )