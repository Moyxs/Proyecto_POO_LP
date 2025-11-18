import json
import logging

from fastapi import HTTPException

from models.customer import Customer
from utils.database import execute_query_json


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)    

async def get_one(id_customer: int) -> Customer:
    sqlscript = """
    SELECT [id_customer],
        [first_name],
        [last_name],
        [age],
        [email]
    FROM [library].[customers]
    WHERE id_customer = ?;
    """
    
    params = [id_customer]

    result_dict = []

    try:
        result = await execute_query_json(sqlscript, params=params)
        result_dict = json.loads(result)


        if len(result_dict) > 0:
            return result_dict[0]
        else:
            raise HTTPException(status_code=404, detail="Customer not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    

async def get_all() -> list[Customer]:
    selectscript = """
    SELECT [id_customer],
        [first_name],
        [last_name],
        [age],
        [email]
    FROM [library].[customers];
 """ 
    result_dict = []
    try:
        result = await execute_query_json(selectscript)
        result_dict = json.loads(result)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def delete_customer(id_customer: int) -> str:
    deletescript = """
    DELETE FROM [library].[customers]
    WHERE id_customer = ?;
    """
    params = [id_customer]

    try:
        await execute_query_json(deletescript, params = params, needs_commit=True)
        return "Book deleted successfully."
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
async def update_customer(customer: Customer) -> Customer:
    
    dict = customer.model_dump(exclude_none=True)

    keys = [k for k in dict.keys() ]
    keys.remove('id_customer')
    variables = " = ?, ".join(keys) + " = ?"

    updatescript = f"""
    UPDATE [library].[customers]
    SET {variables}
    WHERE id_customer = ?;
    """
    params = [dict[v] for v in keys]
    params.append(customer.id_customer)

    update_result = None
    try:
        update_result = await execute_query_json(updatescript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    sqlfind = """
    SELECT [id_customer],
        [first_name],
        [last_name],
        [age],
        [email]
    FROM [library].[customers]
    WHERE id_customer = ?
    """
    params = [customer.id_customer]
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


async def create_customer(customer: Customer) -> Customer:
    sqlscript = """
    INSERT INTO [library].[customers] ([first_name], [last_name], [age], [email] )
    VALUES ( ?, ?, ?, ? );

    """
    params = [
        customer.first_name,
        customer.last_name,
        customer.age,
        customer.email
    ]

    insert_result = None
    try:
        insert_result = await execute_query_json(sqlscript, params, needs_commit=True)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    sqlfind = """
    SELECT [id_customer],
        [first_name],
        [last_name],
        [age],
        [email]
    FROM [library].[customers]
    WHERE email = ?;

    """
    
    params = [customer.email]

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