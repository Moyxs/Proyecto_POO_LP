import json
import logging
from datetime import date

from fastapi import HTTPException
from models.author_books import Author_book
from models.loan_books import Loan_Books
from models.books import Books
from utils.database import execute_query_json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

async def get_one(id_book: int) -> Books:
    sqlscript = """
    SELECT [id],
        [id_genre],
        [isbn],
        [title],
        [its_active],
        [date_published]
    FROM [library].[books]
    WHERE idk = ?;
    """
    
    params = [id_book]

    result_dict = []

    try:
        result = await execute_query_json(sqlscript, params=params)
        result_dict = json.loads(result)


        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Book not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

async def get_all() -> list[Books]:
    selectscript = """
    SELECT [id],
        [id_genre],
        [title],
        [isbn],
        [date_published],
        [its_active]
    FROM [library].[books];    

 """ 
    result_dict = []
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def delete_books(id_book: int) -> str:
    deletescript = """
    DELETE FROM [library].[books]
    WHERE id = ?;
    """
    params = [id_book]

    try:
        await execute_query_json(deletescript, params = params, needs_commit=True)
        return "Book deleted successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_books(books: Books) -> Books:
    
    dict = books.model_dump(exclude_none=True)

    keys = [k for k in dict.keys() ]
    keys.remove('id')
    variables = " = ?, ".join(keys) + " = ?"

    updatescript = f"""
    UPDATE [library].[books]
    SET {variables}
    WHERE id = ?;
    """
    params = [dict[v] for v in keys]
    params.append(books.id)

    update_result = None
    try:
        update_result = await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    sqlfind = """
    SELECT [id],
        [id_genre],
        [isbn],
        [title],
        [its_active],
        [date_published]
    FROM [library].[books]
    WHERE id = ?
    """
    params = [books.id]
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


async def create_books(books: Books) -> Books:
    sqlscript = """
    INSERT INTO [library].[books] ([id_genre], [isbn], [title], [its_active], [date_published])
    VALUES (?, ?, ?, ?, ?);
    """
    params = [
        books.id_genre,
        books.isbn,
        books.title,
        books.its_active,
        books.date_published
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind = """
    SELECT [id],
        [id_genre],
        [isbn],
        [title],
        [its_active],
        [date_published]
    FROM [library].[books]
    WHERE isbn = ?

    """
    
    params = [books.isbn]

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

## BOOKS WITH AUTHORS INTERACTION FUNCTIONS ##

async def get_all_authors(id_book : int ) -> list[Author_book]:
    select_script = """
        SELECT
            ab.id_author
            , a.first_name
            , a.last_name
            , b.date_published
        FROM library.authors_books ab
        inner join library.authors a
        on ab.id_author = a.id
        inner join library.books b
        on ab.id_book = b.id
        WHERE ab.id_book = ?
    """

    params = [id_book]

    try:
        result = await execute_query_json(select_script, params=params)
        print("Raw result:", result)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No authors found for the book")

        return dict_result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }") 
    

## BOOKS WITH LOANS INTERACTION FUNCTIONS ##
async def get_all_loans(id_book: int) -> list[Loan_Books]:
    select_script = """
        SELECT
            l.id
            , l.id_customer
            , lb.return_status
            , l.loan_active
            , l.date_loan
            , l.date_devolution
        FROM library.loans l
        inner join library.loan_books lb
        on l.id = lb.id_loan
        WHERE lb.id_book = ?
    """

    params = [id_book]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No loans found for the book")

        return dict_result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }") 