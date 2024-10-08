from typing import List

from fastapi import FastAPI, Depends, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete, func, update
from starlette import status

from models import get_async_session, Products, Units, Warehouse
from schemas import Unit, Warehouses, WarehouseResponse, UnitResponse, ProductsResponse, ProductsCreate

from faststream import FastStream, Logger
from faststream.kafka import KafkaBroker



app = FastAPI()




broker = KafkaBroker("localhost:9092")
appkafka = FastStream(broker)

store_router = APIRouter(prefix="/store", tags=["Store"])
unit_router = APIRouter(prefix="/unit", tags=["Unit"])
warehouse_router = APIRouter(prefix="/warehouse", tags=["Warehouse"])


@broker.subscriber("user-topic")
async def get_user_token(result):
    if result is None:
        return False
    else:
        return True


''' Find product by Id '''
@store_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=List[ProductsResponse])
async def get_product_by_id(id: int, session: Session = Depends(get_async_session)):
    query = select(Products).where(Products.product_id == id)
    result = await session.execute(query)
    return result.mappings().all()

''' Select all products '''
@store_router.get("/p/all", status_code=status.HTTP_200_OK, response_model=List[ProductsResponse])
async def get_all_product(session: Session = Depends(get_async_session)):
    query = select(Products).order_by(Products.name.asc())
    result = await session.execute(query)
    return result

''' Add product '''
@store_router.post("/add", status_code=status.HTTP_200_OK)
async def add_product(product: ProductsCreate, session: Session = Depends(get_async_session)):
    try:
        query = insert(Products).values(**product.dict())
        result = await session.execute(query)
        await session.commit()
        return {"status" : "ok"}
    except Exception as ex:
        return {"error" : str(ex)}

''' Update product '''
@store_router.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_product(product: ProductsCreate, id: int, session: Session = Depends(get_async_session)):
    try:
        query = update(Products).where(Products.product_id == id).values(**product.dict())
        result = await session.execute(query)
        await session.commit()
        return {"result" : "ok"}
    except Exception as ex:
        return {"error" : str(ex)}

''' Delete product '''
@store_router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_product(id: int, session: Session = Depends(get_async_session)):
    try:
        query = delete(Products).where(Products.product_id == id)
        result = await session.execute(query)
        await session.commit()
        return {"result" : "ok"}
    except Exception as ex:
        return {"error" : str(ex)}

''' Select all units '''
@unit_router.get("/u/all", status_code=status.HTTP_200_OK, response_model=List[UnitResponse])
async def get_all_units(session: Session = Depends(get_async_session)):
    query = select(Units).order_by(Units.unit_name)
    result = await session.execute(query)
    return result

''' Find unit by Id '''
@unit_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=List[UnitResponse])
async def get_unit_by_id(id: int, session: Session = Depends(get_async_session)):
    query = select(Units).where(Units.unit_id == id)
    result = await session.execute(query)
    return result.mappings().all()


''' Add unit '''
@unit_router.post("/add", status_code=status.HTTP_200_OK)
async def add_unit(unit: Unit, session: Session = Depends(get_async_session)):
    try:
        query = insert(Units).values(**unit.dict())
        result = await session.execute(query)
        await session.commit()
        return {"status" : "ok"}
    except Exception as ex:
        return {"error" : str(ex)}

''' Update unit '''
@unit_router.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_unit(unit: Unit, id: int, session: Session = Depends(get_async_session)):
    try:
        query = update(Units).where(Units.unit_id == id).values(**unit.dict())
        result = await session.execute(query)
        await session.commit()
        return {"result" : "ok"}
    except Exception as ex:
        return {"error" : str(ex)}

''' Delete unit '''
@unit_router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_unit(id: int, session: Session = Depends(get_async_session)):
    try:
        query = delete(Units).where(Units.unit_id == id)
        result = await session.execute(query)
        await session.commit()
        return {"result" : "ok"}
    except Exception as ex:
        return {"error" : str(ex)}

''' Select all warehouses '''
@warehouse_router.get("/w/all", status_code=status.HTTP_200_OK, response_model=List[WarehouseResponse])
async def get_all_units(session: Session = Depends(get_async_session)):
    query = select(Warehouse).order_by(Warehouse.warehouse_id)
    result = await session.execute(query)
    return result

''' Find warehouse by Id '''
@warehouse_router.get("/{id}", status_code=status.HTTP_200_OK, response_model=List[WarehouseResponse])
async def get_unit_by_id(id: int, session: Session = Depends(get_async_session)):
    query = select(Warehouse).where(Warehouse.warehouse_id == id)
    result = await session.execute(query)
    return result.mappings().all()


''' Add warehouse '''
@warehouse_router.post("/add", status_code=status.HTTP_200_OK)
async def add_unit(warehouse: Warehouses, session: Session = Depends(get_async_session)):
    try:
        query = insert(Warehouse).values(**warehouse.dict())
        result = await session.execute(query)
        await session.commit()
        return {"status" : "ok"}
    except Exception as ex:
        return {"error" : str(ex)}

''' Update warehouse '''
@warehouse_router.put("/update/{id}", status_code=status.HTTP_200_OK)
async def update_unit(warehouse: Warehouses, id: int, session: Session = Depends(get_async_session)):
    try:
        query = update(Warehouse).where(Warehouse.warehouse_id == id).values(**warehouse.dict())
        result = await session.execute(query)
        await session.commit()
        return {"result" : "ok"}
    except Exception as ex:
        return {"error" : str(ex)}

''' Delete unit '''
@warehouse_router.delete("/delete/{id}", status_code=status.HTTP_200_OK)
async def delete_unit(id: int, session: Session = Depends(get_async_session)):
    try:
        query = delete(Warehouse).where(Warehouse.warehouse_id == id)
        result = await session.execute(query)
        await session.commit()
        return {"result" : "ok"}
    except Exception as ex:
        return {"error" : str(ex)}

app.include_router(store_router)
app.include_router(unit_router)
app.include_router(warehouse_router)