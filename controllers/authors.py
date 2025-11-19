import json
import logging

from fastapi import HTTPException
from models.authors import Author
from models.author_books import Author_book
from utils.database import execute_query_json



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

async def get_one(id: int) -> Author:
    sqlscript = """
    SELECT [id], 
    [first_name], 
    [last_name]
    FROM [library].[authors]
    WHERE id = ? 
    """
    
    params = [id]

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
     SELECT [id],
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
    WHERE id = ?;
    """
    params = [id]

    try:
        await execute_query_json(deletescript, params = params, needs_commit=True)
        return "Author deleted successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_author(authors: Author) -> Author:
    
    dict = authors.model_dump(exclude_none=True)

    keys = [k for k in dict.keys() ]
    keys.remove("id")
    vaiables = " = ?, ".join(keys) + " = ?"

    updatescript = f"""
    UPDATE [library].[authors]
    SET {vaiables}
    WHERE id = ?;
    """
    params = [dict[v] for v in keys]
    params.append(authors.id)

    update_result = None
    try:
        update_result = await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    sqlfind = """
    SELECT [id],
    [first_name], 
    [last_name]
    FROM [library].[authors]
    WHERE id = ? 
    """
    params = [authors.id]
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
    SELECT [id], 
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
    
## AUTHORS WITH BOOKS INTERACTION FUNCTIONS ##
async def get_all_books(id_author: int) -> list[Author_book]:
    select_script = """
        SELECT
            ab.id_book
            , b.title
            , b.date_published
        FROM library.authors_books ab
        inner join library.books b
        on ab.id_book =b.id
        WHERE ab.id_author = ?
    """

    params = [id_author]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No books found for the author")

        return dict_result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def get_one_book(id_author: int, id_book: int) -> Author_book:
    select_script = """
        SELECT
            b.id_genre
            , b.title
            , b.date_published
            , b.isbn
            , b.its_active
        FROM library.books b
        inner join library.authors_books ab 
        on b.id = ab.id_book
        WHERE ab.id_author = ?
        and b.id = ?;
    """

    params = [id_author, id_book]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No book found for the author")

        return dict_result[0]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def add_book_to_author(id_author: int, id_book: int) -> Author_book:

    insert_script = """
        INSERT INTO [library].[authors_books] ([id_author], [id_book])
        VALUES (?, ?);
    """

    params = [
        id_author,
        id_book
    ]

    try:
        await execute_query_json(insert_script, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    select_script = """
        SELECT
            b.id
            , b.id_genre
            , b.title
            , b.date_published
            , b.isbn
            , b.its_active
        FROM library.books b
        inner join library.authors_books ab 
        on b.id = ab.id_book
        WHERE b.id = ?
        and ab.id_author = ?;
    """

    params = [id_book, id_author]

    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def remove_book_from_author(id_author: int, id_book: int) -> str:
    delete_script = """
        DELETE FROM [library].[authors_books]
        WHERE [id_author] = ? AND [id_book] = ?;
    """

    params = [id_author, id_book]

    try:
        await execute_query_json(delete_script, params=params, needs_commit=True)
        return "BOOK FROM AUTHOR REMOVED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")