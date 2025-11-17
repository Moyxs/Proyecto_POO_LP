import json
import logging

from fastapi import HTTPException

from models import author_books
from models.authors import Author
from models.author_books import Author_book

from utils.database import execute_query_json



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

async def get_one(id_author: int) -> Author:
    sqlscript = """
    SELECT [id_author], 
    [first_name], 
    [last_name]
    FROM [library].[authors]
    WHERE id_author = ? 
    """
    
    params = [id_author]

    result_dict = []

    try:
        result = await execute_query_json(sqlscript, params=params)
        result_dict = json.loads(result)


        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Author not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

async def get_all() -> list[Author]:
    selectscript = """
     SELECT [id_author],
        [first_name], 
         [last_name]
         FROM [library].[authors]
 """ 
    result_dict = []
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def delete_author(id_author: int) -> str:
    deletescript = """
    DELETE FROM [library].[authors]
    WHERE id_author = ?;
    """
    params = [id_author]

    try:
        await execute_query_json(deletescript, params = params, needs_commit=True)
        return "Author deleted successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_author(authors: Author) -> Author:
    
    dict = authors.model_dump(exclude_none=True)

    keys = [k for k in dict.keys() ]
    keys.remove("id_author")
    vaiables = " = ?, ".join(keys) + " = ?"

    updatescript = f"""
    UPDATE [library].[authors]
    SET {vaiables}
    WHERE id_author = ?;
    """
    params = [dict[v] for v in keys]
    params.append(authors.id_author)

    update_result = None
    try:
        update_result = await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    sqlfind = """
    SELECT [id_author],
    [first_name], 
    [last_name]
    FROM [library].[authors]
    WHERE first_name = ? 
    """
    params = [authors.first_name]
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


async def create_author(authors: Author) -> Author:
    sqlscript = """
    INSERT INTO [library].[authors] ([first_name], [last_name])
    VALUES (?, ?);
    """
    params = [
        authors.first_name,
        authors.last_name 
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind = """
    SELECT [id_author], 
    [first_name], 
    [last_name]
    FROM [library].[authors]
    WHERE first_name = ? 
    """
    
    params = [authors.first_name]

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