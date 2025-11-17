from fastapi import APIRouter, status

from models.authors import Author

from controllers.authors import (
    create_author
    , update_author
    , delete_author
    , get_all
    , get_one

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


