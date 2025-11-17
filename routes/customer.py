from fastapi import APIRouter, status

from models.customer import Customer

from controllers.customer import (
    create_customer
    , update_customer
    , delete_customer
    , get_all
    , get_one

)

router = APIRouter(prefix="/customer")

@router.get("/" , tags=["customer"], status_code=status.HTTP_200_OK )
async def get_all_customers():
    result = await get_all()
    return result

@router.post("/", tags=["customer"], status_code=status.HTTP_201_CREATED)
async def create_new_customer(customer_data: Customer):
    result = await create_customer(customer_data)
    return result

@router.put("/", tags=["customer"], status_code=status.HTTP_201_CREATED)
async def update_customer_information(customer_data: Customer, id_customer: int):
    customer_data.id_customer = id_customer
    result = await update_customer(customer_data)
    return result

@router.delete("/{id_customer}", tags=["customer"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer_by_id(id_customer: int):
    status : Customer = await delete_customer(id_customer)
    return status

@router.get("/{id_customer}", tags=["customer"], status_code=status.HTTP_200_OK)
async def get_one_customer(id_customer: int):
    result : Customer = await get_one(id_customer)
    return result
