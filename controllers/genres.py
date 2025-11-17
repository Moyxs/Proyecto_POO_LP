import json
import logging

from fastapi import HTTPException

from models.genres import Genres
from utils.database import execute_query_json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

async def get_one(id_genres: int) -> Genres:
    sqlscript = """
    SELECT [id_genres],
        [name_genre],
        [description]       
    FROM [library].[genres]
    WHERE id_genres = ?;
    """
    
    params = [id_genres]

    result_dict = []

    try:
        result = await execute_query_json(sqlscript, params=params)
        result_dict = json.loads(result)


        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Genre not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

async def get_all() -> list[Genres]:
    selectscript = """
    SELECT [id_genres],
        [name_genre],
        [description]
    FROM [library].[genres];
 """ 
    result_dict = []
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def delete_genres(id_genres: int) -> str:
    deletescript = """
    DELETE FROM [library].[genres]
    WHERE id_genres = ?;
    """
    params = [id_genres]

    try:
        await execute_query_json(deletescript, params = params, needs_commit=True)
        return "Genre deleted successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_genres(genres: Genres) -> Genres:
    
    dict = Genres.model_dump(exclude_none=True)

    keys = [k for k in dict.keys() ]
    keys.remove("id_genres")
    vaiables = " = ?, ".join(keys) + " = ?"

    updatescript = f"""
    UPDATE [library].[genres]
    SET {vaiables}
    WHERE id_genres = ?;
    """
    params = [dict[v] for v in keys]
    params.append(genres.id_genres)

    update_result = None
    try:
        update_result = await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    sqlfind = """
    SELECT [id_genres],
        [name_genre],
        [description]
    FROM [library].[genres]
    WHERE id_genres = ?;
    """
    params = [Genres.name_genre]
    result_dict = []
    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)


        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


async def create_genres(genres: Genres) -> Genres:
    sqlscript = """
    INSERT INTO [library].[customer] ([first_name], [last_name], [email], [phone_number], [its_active] )
    VALUES (?, ?, ?, ?, ?);
    """
    params = [
        genres.name_genre,
        genres.description
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind = """
    SELECT [id_genres],
        [name_genre],
        [description]
    FROM [library].[genres]
    WHERE name_genre = ?;

    """
    
    params = [genres.name_genre]

    result_dict = []

    try:
        result = await execute_query_json(sqlfind, params=params)
        result_dict = json.loads(result)


        if len(result_dict) > 0:
            return result_dict[0]
        else:
            return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")   