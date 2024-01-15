from fastapi import Depends, HTTPException, APIRouter, UploadFile, File, Form, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from dateutil.relativedelta import relativedelta
import pandas as pd
from .admin_crud import AdminItemCrud
from app.db import PDENGINE
from app.db import getSession
import os
from datetime import datetime, timedelta
from app.models import ItemBase, ItemDetails, SearchFilters, Item
from app.items.crud import ItemCrud
from ..utils.email_utils import send_order_report

router = APIRouter()

@router.get("/item/count")
async def item_count(session: AsyncSession = Depends(getSession)):
    """Returns total item count to calculate total pages"""
    return await ItemCrud.item_count(session=session)

@router.post("/upload")
async def upload_file(file: UploadFile, session: AsyncSession = Depends(getSession)):
    """will read a csv/json and write to database new or existing items"""
    try:
        if file.content_type == 'application/json':
            df = pd.read_json(file.file)
        else:
            df = pd.read_csv(file.file)
        df.fillna('', inplace=True)
        df['price'] = df['price'].astype(float)
        df['in_stock'] = df['in_stock'].astype(int)
        df['barcode'] = df['barcode'].astype(str)
        items = df.to_dict(orient="records")
        await ItemCrud.items_from_import(items, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.put("/item")
async def update_item(item: Item, session: AsyncSession = Depends(getSession)):
    """updates one item"""
    try:
       return await AdminItemCrud.update_item(item=item, session=session)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.delete("/item/{barcode}", status_code=204)
async def delete_item(barcode:str, session: AsyncSession = Depends(getSession)):
    try:
        await AdminItemCrud.delete_item(barcode=barcode, session=session)
        return 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
    
@router.post("/item", status_code=201)
async def add_item(item: ItemDetails, session: AsyncSession = Depends(getSession)):
    """adds one item"""
    try:
        result = await AdminItemCrud.create_item(item=item, session=session)
        return result
    except Exception as e:
        raise HTTPException(status_code=500) from e