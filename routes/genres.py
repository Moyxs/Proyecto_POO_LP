from fastapi import APIRouter, status

from models.genres import Genres

from controllers.genres import (
    create_genres
    , update_genres
    , delete_genres
    , get_all
    , get_one


)

router = APIRouter(prefix="/genres")

@router.get("/" , tags=["Genres"], status_code=status.HTTP_200_OK )
async def get_all_genres():
    result = await get_all()
    return result

@router.post("/", tags=["Genres"], status_code=status.HTTP_201_CREATED)
async def create_new_genres(genres_data: Genres):
    result = await create_genres(genres_data)
    return result

@router.put("/", tags=["Genres"], status_code=status.HTTP_201_CREATED)
async def update_genres_information(genres_data: Genres, id_genres: int):
    genres_data.id_genres = id_genres
    result = await update_genres(genres_data)
    return result

@router.delete("/{id_genres}", tags=["Genres"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_genres_by_id(id_genres: int):
    status : Genres = await delete_genres(id_genres)
    return status

@router.get("/{id_genres}", tags=["Genres"], status_code=status.HTTP_200_OK)
async def get_one_genres(id_genres: int):
    result : Genres = await get_one(id_genres)
    return result
