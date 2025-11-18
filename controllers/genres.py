import json
import logging

from fastapi import HTTPException

from models.genres import Genres
from utils.database import execute_query_json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

async def get_one(id_genres: int) -> Genres:
    sqlscript = """
    SELECT [id_genre],
        [name_genres],
        [description]       
    FROM [library].[genres]
    WHERE id_genre = ?;
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
    SELECT [id_genre],
        [name_genres],
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
    
async def delete_genres(id_genre: int) -> str:
    deletescript = """
    DELETE FROM [library].[genres]
    WHERE id_genre = ?;
    """
    params = [id_genre]

    try:
        await execute_query_json(deletescript, params = params, needs_commit=True)
        return "Genre deleted successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_genres( genres: Genres) -> Genres:
    
    dict = genres.model_dump(exclude_none=True)

    keys = [ k for k in dict.keys() ]
    keys.remove('id_genres')
    variables = " = ?, ".join(keys) + " = ?"

    updatescript = f"""
    UPDATE [library].[genres]
    SET {variables}
    WHERE [id_genre] = ?;
    """

    params = [dict[v] for v in keys]
    params.append( genres.id_genres )

    update_result = None
    try:
        update_result = await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    sqlfind = """
    SELECT [id_genre],
           [name_genres],
           [description]
    FROM [library].[genres]
    WHERE id_genre = ?;
    """

    params = [genres.id_genres]

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
    INSERT INTO [library].[genres] ([name_genres], [description])
    VALUES (?, ?);
    """
    params = [
        genres.name_genres,
        genres.description
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind = """
    SELECT [id_genre],
        [name_genres],
        [description]
    FROM [library].[genres]
    WHERE name_genres = ?;

    """
    
    params = [genres.name_genres]

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