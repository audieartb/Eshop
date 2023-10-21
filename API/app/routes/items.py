from app.db import getSession
from app.models import Items, ItemsCreate, ItemsDetails
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ..crud.items import ItemCrud as crud

router = APIRouter()


@router.get("/items", response_model=list[Items])
async def get_items(skip: int = 0, limit: int = 15, session: AsyncSession = Depends(getSession)):
    try:
        result = await crud.get_items(limit=limit, skip=skip,  session=session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/items/{item_id}")
async def item_by_id(item_id=str, session: AsyncSession = Depends(getSession)):
    """item by id receives the barcode"""
    try:
        item = await crud.item_by_id(item_id, session=session)
        if (item is None):
            raise HTTPException(status_code=404, detail="Item not found")
        return {"item": item}
    except Exception as e:
        raise HTTPException(status_code=500) from e


@router.get("/items/search")
async def search_items(session: AsyncSession = Depends(getSession)):
    pass


@router.post("/items", status_code=201)
async def add_item(item: ItemsCreate, session: AsyncSession = Depends(getSession)):
    try:
        result = await crud.add_item(item=item, session=session)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500) from e


@router.put("/items", status_code=204)
async def update_item(item: Items, session: AsyncSession = Depends(getSession)):
    try:
        await crud.update_item_sold(item_id=item.id, sold=item.sold, session=session)
        return
    except Exception as e:
        raise HTTPException(status_code=500) from e
