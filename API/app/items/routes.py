from app.db import getSession
from app.models import Item, ItemBase, ItemDetails
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from .crud import ItemCrud

router = APIRouter()


@router.get("/items", response_model=list[Item])
async def get_items(skip: int = 0, limit: int = 15, price_from: int | None = None,
                    price_to: int | None = None, search: str = '', session: AsyncSession = Depends(getSession)):
    """Handles all requests to search multiple items"""
    try:
        result = await ItemCrud.get_items(limit=limit, skip=skip, price_from=price_from, price_to=price_to, search=search,   session=session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/items/{item_id}")
async def item_by_id(item_id=str, session: AsyncSession = Depends(getSession)):
    """item by id receives the barcode"""
    try:
        item = await ItemCrud.item_by_id(barcode=item_id, session=session)
        if (item is None):
            raise HTTPException(status_code=404, detail="Item not found")
        return {"item": item}
    except Exception as e:
        raise HTTPException(status_code=500) from e


@router.post("/items", status_code=201)
async def add_item(item: Item, session: AsyncSession = Depends(getSession)):
    """adds one item"""
    try:
        result = await ItemCrud.add_item(item=item, session=session)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500) from e


@router.put("/items", status_code=204)
async def update_item(item: Item, session: AsyncSession = Depends(getSession)):
    """updates one item"""
    try:
        await ItemCrud.update_item_sold(item_id=item.id, sold=item.sold, session=session)
        return
    except Exception as e:
        raise HTTPException(status_code=500) from e


@router.post("/itemsbulk", status_code=200)
async def add_bulk(items: list[ItemDetails], session: AsyncSession = Depends(getSession)):
    try:
        result = await ItemCrud.create_items(items=items, session=session)
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
