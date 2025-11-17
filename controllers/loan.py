import json
import logging

from fastapi import HTTPException

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
    FROM [library].[loan]
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
    FROM [library].[loan];
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
    DELETE FROM [library].[loan]
    WHERE id_loan = ?;
    """
    params = [id_loan]

    try:
        await execute_query_json(deletescript, params = params, needs_commit=True)
        return "Loan deleted successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_loan(loan: Loan) -> Loan:
    
    dict = Loan.model_dump(exclude_none=True)

    keys = [k for k in dict.keys() ]
    keys.remove("id_loan")
    vaiables = " = ?, ".join(keys) + " = ?"

    updatescript = f"""
    UPDATE [library].[loan]
    SET {vaiables}
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
    FROM [library].[loan]
    WHERE id_loan = ?;
    """
    params = [Loan.title]
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
    INSERT INTO [library].[loan] ([id_customer], [date_loan], [date_devolution], [loan_active] )
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
    FROM [library].[loan]
    WHERE id_loan = ?;
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
    


    #*****************************************************
    #loan_books