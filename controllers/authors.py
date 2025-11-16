import json
import logging

from models.author import Author
from utils.database import execute_query_json
from fastapi import HTTPException

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

async def create_author(author: Author) -> Author:
    sqlscript = """
    INSERT INTO [library].[authors] ([first_name], [last_name], [nationality])
    VALUES (?, ?, ?);
    """
    params = [
        author.first_name,
        author.last_name, 
        author.nationality
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind = """
    SELECT [id_author], 
    [first_name], 
    [last_name], 
    [nationality]
    FROM [library].[authors]
    WHERE nationality = ? 
    """
    
    params = [author.nationality]

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