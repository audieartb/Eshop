from app.db import getSession
from app.models import Item, ItemDetails
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from .crud import ItemCrud

router = APIRouter()


@router.get("/items", response_model=list[Item], tags=['Items Client'])
async def get_items(skip: int = 0, limit: int | None = None, price_from: int | None = None,
                    price_to: int | None = None, search: str = '', session: AsyncSession = Depends(getSession)):
    """Handles all requests to search multiple items"""
    try:
        result = await ItemCrud.get_items(limit=limit, skip=skip, price_from=price_from, price_to=price_to, search=search, session=session)
        print(result)
        if not result:
            print('raising 404')
            raise HTTPException(
                status_code=404, detail='No items matching your search parameters')
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/items/{item_id}", tags=['Items Client'])
async def item_by_id(item_id=str, session: AsyncSession = Depends(getSession)):
    """item by id receives the barcode"""
    try:
        item = await ItemCrud.item_by_id(barcode=item_id, session=session)
        if (item is None):
            raise HTTPException(status_code=404, detail="Item not found")
        return {"item": item}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/itemsbulk", status_code=200, tags=['Items Client'])
async def add_bulk(items: list[ItemDetails], session: AsyncSession = Depends(getSession)):
    try:
        result = await ItemCrud.create_items(items=items, session=session)
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
