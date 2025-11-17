from fastapi import APIRouter, status

from models.authors import Author
from models.author_books import Author_book

from controllers.authors import (
    create_author
    , update_author
    , delete_author
    , get_all
    , get_one
    , get_all_books
    , get_one_book
    , add_book_to_author
    , remove_book_from_author

)

router = APIRouter(prefix="/authors")

@router.get("/" , tags=["authors"], status_code=status.HTTP_200_OK )
async def get_all_authors():
    result = await get_all()
    return result

@router.post("/", tags=["authors"], status_code=status.HTTP_201_CREATED)
async def create_new_author(author_data: Author):
    result = await create_author(author_data)
    return result

@router.put("/", tags=["authors"], status_code=status.HTTP_201_CREATED)
async def update_author_information(author_data: Author, id_author: int):
    author_data.id_author = id_author
    result = await update_author(author_data)
    return result

@router.delete("/{id_author}", tags=["authors"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_author_by_id(id_author: int):
    status : Author = await delete_author(id_author)
    return status

@router.get("/{id_author}", tags=["authors"], status_code=status.HTTP_200_OK)
async def get_one_author(id_author: int):
    result : Author = await get_one(id_author)
    return result

## AUTHORS WITH BOOKS INTERACTION FUNCTIONS ##
@router.get("/{id_author}/books", tags=["authors"], status_code=status.HTTP_200_OK)
async def get_all_books_of_author( id_author: int ):
    result = await get_all_books(id_author)
    return result

@router.get("/{id_author}/books/{id_book}", tags=["authors"], status_code=status.HTTP_200_OK)
async def get_one_book_of_author( id_author: int, id_book: int ):
    result = await get_one_book(id_author, id_book)
    return result

@router.post("/{id_author}/books", tags=["authors"], status_code=status.HTTP_201_CREATED)
async def assign_book_to_author( id_author: int, book_data: Author_book ):
    result = await add_book_to_author(id_author, book_data.id_book)
    return result

@router.delete("/{id_author}/books/{id_book}", tags=["authors"], status_code=status.HTTP_204_NO_CONTENT)
async def remove_book_from_author_id( id_author: int, id_book: int ):
    status: str =  await remove_book_from_author(id_author, id_book)
    return status
