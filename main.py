import uvicorn 
from typing import Union
from fastapi import FastAPI
from utils.database import execute_query_json
import os
import json


app = FastAPI()


@app.get("/")
def read_root():
    return {
        "Hello": "World",
        "version": "0.1.0"
    }


@app.get("/authors/")
async def get_all_authors():
    sqlscript= """
  SELECT [id_author]
      ,[first_name]
      ,[last_name]
      ,[nationality]
  FROM [library].[authors]
"""
    result = await execute_query_json(sqlscript)
    result_dict = json.loads(result)
    return result_dict

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")