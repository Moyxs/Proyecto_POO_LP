import json
import logging

from fastapi import HTTPException
from models.loan_books import Loan_Books
from models.loan import Loan
from utils.database import execute_query_json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

async def get_one(id_loan: int) -> Loan:
    sqlscript = """
    SELECT [id_loan],
        [id_customer],
        [date_loan],
        [date_devolution],
        [loan_active]
    FROM [library].[loans]
    WHERE id_loan = ?;
    """
    
    params = [id_loan]

    result_dict = []

    try:
        result = await execute_query_json(sqlscript, params=params)
        result_dict = json.loads(result)


        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Loan not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

async def get_all() -> list[Loan]:
    selectscript = """
    SELECT [id_loan],
        [id_customer],
        [date_loan],
        [date_devolution],
        [loan_active]
    FROM [library].[loans];
 """ 
    result_dict = []
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def delete_loan(id_loan: int) -> str:
    deletescript = """
    DELETE FROM [library].[loans]
    WHERE id_loan = ?;
    """
    params = [id_loan]

    try:
        await execute_query_json(deletescript, params = params, needs_commit=True)
        return "Loan deleted successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_loan(loan: Loan) -> Loan:
    
    dict = loan.model_dump(exclude_none=True)

    keys = [k for k in dict.keys() ]
    keys.remove('id_loan')
    variables = " = ?, ".join(keys) + " = ?"

    updatescript = f"""
    UPDATE [library].[loans]
    SET {variables}
    WHERE id_loan = ?;
    """
    params = [dict[v] for v in keys]
    params.append(loan.id_loan)

    update_result = None
    try:
        update_result = await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    sqlfind = """
    SELECT [id_loan],
        [id_customer],
        [date_loan],
        [date_devolution],
        [loan_active]
    FROM [library].[loans]
    WHERE id_loan = ?;
    """
    params = [loan.id_loan]
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


async def create_loan(loan: Loan) -> Loan:
    sqlscript = """
    INSERT INTO [library].[loans] ([id_customer], [date_loan], [date_devolution], [loan_active] )
    VALUES (?, ?, ?, ?);

    """
    params = [
        loan.id_customer,
        loan.date_loan,
        loan.date_devolution,
        loan.loan_active
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind = """
    SELECT [id_loan],
        [id_customer],
        [date_loan],
        [date_devolution],
        [loan_active]
    FROM [library].[loans]
    WHERE id_customer = ?;
    """
    
    params = [loan.id_customer]

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
    


## LOANS WITH BOOKS INTERACTION FUNCTIONS ##
async def get_all_books(id_loan: int) -> list[Loan_Books]:
    select_script = """
        SELECT
            b.id_book
            , b.title
            , b.date_published
            , b.isbn
            , lb.return_status
        FROM library.books b
        inner join library.loan_books lb
        on b.id_book =lb.id_book
        WHERE lb.id_loan = ?
    """

    params = [id_loan]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No books found for the loan")

        return dict_result
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def get_one_book(id_loan: int, id_book: int) -> Loan_Books:
    select_script = """
        SELECT
            b.id_book
            , b.id_genre
            , b.title
            , b.date_published
            , b.isbn
            , lb.return_status
        FROM library.books b
        inner join library.loan_books lb 
        on b.id_book = lb.id_book
        WHERE lb.id_loan = ?
        and b.id_book = ?;
    """

    params = [id_loan, id_book]

    try:
        result = await execute_query_json(select_script, params=params)
        dict_result = json.loads(result)
        if len(dict_result) == 0:
            raise HTTPException(status_code=404, detail="No book found for the loan")

        return dict_result[0]
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Database error: { str(e) }")
    
async def add_book_to_loan(id_loan: int, id_book: int) -> Loan_Books:

    insert_script = """
        INSERT INTO [library].[loan_books] ([id_loan], [id_book])
        VALUES (?, ?);
    """

    params = [
        id_loan,
        id_book
    ]

    try:
        await execute_query_json(insert_script, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    select_script = """
        SELECT
            b.id_book
            , b.id_genre
            , b.title
            , b.date_published
            , b.isbn
            , b.its_active
        FROM library.books b
        inner join library.loan_books lb 
        on b.id_book = lb.id_book
        WHERE b.id_book = ?
        and lb.id_loan = ?;
    """

    params = [id_book, id_loan]

    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def remove_book_from_loan(id_loan: int, id_book: int) -> str:
    delete_script = """
        DELETE FROM [library].[loan_books]
        WHERE [id_loan] = ? AND [id_book] = ?;
    """

    params = [id_loan, id_book]

    try:
        await execute_query_json(delete_script, params=params, needs_commit=True)
        return "BOOK FROM LOAN REMOVED"
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")
    
async def update_book_info(book_data: Loan_Books) -> Loan_Books:
    dict = book_data.model_dump(exclude_none=True)
    keys = [ k for k in  dict.keys() ]
    keys.remove('id_loan')
    keys.remove('id_book')
    variables = " = ?, ".join(keys)+" = ?"

    updatescript = f"""
        UPDATE [library].[loan_books]
        SET {variables}
        WHERE [id_loan] = ? AND [id_book] = ?;
    """

    params = [ dict[v] for v in keys ]
    params.append( book_data.id_loan )
    params.append( book_data.id_book )

    try:
        await execute_query_json( updatescript, params, needs_commit=True )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")

    select_script = """
        SELECT
            b.id_genre
            , b.title
            , b.date_published
            , b.isbn
            , lb.return_status
        FROM library.books b
        inner join library.loan_books lb 
        on b.id_book = lb.id_book
        WHERE lb.id_loan = ?
        and b.id_book = ?;
    """

    params = [book_data.id_loan, book_data.id_book]

    try:
        result = await execute_query_json(select_script, params=params)
        return json.loads(result)[0]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: { str(e) }")