from fastapi import APIRouter, status

from models.loan import Loan
from models.loan_books import Loan_Books

from controllers.loan import (
    create_loan
    , update_loan
    , delete_loan
    , get_all
    , get_one
    , get_all_books
    , get_one_book
    , add_book_to_loan
    , update_book_info
    , remove_book_from_loan
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

## LOANS WITH BOOKS INTERACTION FUNCTIONS ##
@router.get("/{id_loan}/books", tags=["loan"], status_code=status.HTTP_200_OK)
async def get_all_books_of_loan( id_author: int ):
    result = await get_all_books(id_author)
    return result

@router.get("/{id_loan}/books/{id_book}", tags=["loan"], status_code=status.HTTP_200_OK)
async def get_one_book_of_loan( id_loan: int, id_book: int ):
    result = await get_one_book(id_loan, id_book)
    return result

@router.post("/{id_loan}/books", tags=["loan"], status_code=status.HTTP_201_CREATED)
async def assign_book_to_loan( id_loan: int, book_data: Loan_Books ):
    result = await add_book_to_loan(id_loan, book_data.id_book)
    return result

@router.put("/{id_loan}/books/{id_book}", tags=["loan"], status_code=status.HTTP_201_CREATED)
async def update_book_of_loan( id_loan: int, id_book: int, book_data: Loan_Books ):
    book_data.id_loan = id_loan
    book_data.id_book = id_book
    result = await update_book_info(book_data)
    return result

@router.delete("/{id_loan}/books/{id_book}", tags=["loans"], status_code=status.HTTP_204_NO_CONTENT)
async def remove_book_from_loan_id( id_loan: int, id_book: int ):
    status: str =  await remove_book_from_loan(id_loan, id_book)
    return status