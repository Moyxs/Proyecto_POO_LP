from fastapi import APIRouter, status

from models.loan import Loan

from controllers.loan import (
    create_loan
    , update_loan
    , delete_loan
    , get_all
    , get_one
)

router = APIRouter(prefix="/loan")

@router.get("/" , tags=["loan"], status_code=status.HTTP_200_OK )
async def get_all_loan():
    result = await get_all()
    return result

@router.post("/", tags=["loan"], status_code=status.HTTP_201_CREATED)
async def create_new_loan(loan_data: Loan):
    result = await create_loan(loan_data)
    return result

@router.put("/", tags=["loan"], status_code=status.HTTP_201_CREATED)
async def update_loan_information(loan_data: Loan, id_loan: int):
    loan_data.id_loan = id_loan
    result = await update_loan(loan_data)
    return result

@router.delete("/{id_loan}", tags=["loan"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_loan_by_id(id_loan: int):
    status : Loan = await delete_loan(id_loan)
    return status

@router.get("/{id_loan}", tags=["loan"], status_code=status.HTTP_200_OK)
async def get_one_loan(id_loan: int):
    result : Loan = await get_one(id_loan)
    return result
