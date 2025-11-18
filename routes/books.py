from fastapi import APIRouter, status

from models.books import Books

from controllers.books import (
    create_books
    , update_books
    , delete_books
    , get_all
    , get_one
    , get_all_authors
    ,get_all_loans
)

router = APIRouter(prefix="/books")

@router.get("/" , tags=["books"], status_code=status.HTTP_200_OK )
async def get_all_books():
    result = await get_all()
    return result

@router.post("/", tags=["books"], status_code=status.HTTP_201_CREATED)
async def create_new_book(book_data: Books):
    result = await create_books(book_data)
    return result

@router.put("/", tags=["books"], status_code=status.HTTP_201_CREATED)
async def update_book_information(book_data: Books, id_book: int):
    book_data.id_book = id_book
    result = await update_books(book_data)
    return result

@router.delete("/{id_book}", tags=["books"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(id_book: int):
    status : Books = await delete_books(id_book)
    return status

@router.get("/{id_book}", tags=["books"], status_code=status.HTTP_200_OK)
async def get_one_book(id_book: int):
    result : Books = await get_one(id_book)
    return result


## BOOKS WITH AUTHORS INTERACTION FUNCTIONS ##
@router.get("/{id_book}/authors", tags=["books"], status_code=status.HTTP_200_OK)
async def get_all_authors_from_book( id_book: int ):
    result = await get_all_authors(id_book)
    return result

## BOOKS WITH LOANS INTERACTION FUNCTIONS ##
@router.get("/{id_book}/loans", tags=["books"], status_code=status.HTTP_200_OK)
async def get_all_loans_from_book( id_book: int ):
    result = await get_all_loans(id_book)
    return result