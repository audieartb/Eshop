from fastapi import Depends, HTTPException, APIRouter, UploadFile, File, Form, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
import pandas as pd
from .admin_crud import AdminItemCrud
from app.db import PDENGINE
from app.db import getSession
import os
from datetime import datetime, timedelta
from app.models import ItemBase, ItemDetails, SearchFilters
from app.items.crud import ItemCrud
from dataclasses import dataclass
import time

router = APIRouter()


def check_file_exists(filename: str):
    if not os.path.exists('db_files'):
        os.makedirs('db_files')

    if not os.path.exists(f'db_files/{filename}.csv'):
        with open(f'db_files/{filename}.csv', 'w+'):
            pass
        return False
    else:
        return True


def get_dataframe(query: str = None, filename: str = ''):

    query_all = 'select * from order_data'
    filename = "orders"

    if not check_file_exists(filename='orders'):
        df = pd.read_sql(query_all, con=PDENGINE)
        df.to_csv(path_or_buf=f'db_files/{filename}.csv')
        return df

    ctime = os.path.getctime(f'db_files/{filename}.csv')
    ctimestamp = datetime.fromtimestamp(ctime)
    # if ((ctimestamp + timedelta(seconds=1)) > datetime.now()):
    if ((ctimestamp) > datetime.now()):
        df = pd.read_csv(f'db_files/{filename}.csv')

        return df
    else:

        df = pd.read_sql(query, con=PDENGINE)
        df.to_csv(path_or_buf=f'db_files/{filename}.csv')
        return df


@router.get("/item/count")
async def item_count(session: AsyncSession = Depends(getSession)):
    return await ItemCrud.item_count(session=session)


@router.get("/order/count")
async def order_count(session: AsyncSession = Depends(getSession)):
    return await AdminItemCrud.get_order_count(session=session)



@router.post("/order")
async def get_orders(filters: SearchFilters, session: AsyncSession = Depends(getSession)):
    all_orders = await AdminItemCrud.get_orders(order_by=filters.order_by,
                                                order_asc=filters.order_asc,
                                                skip=filters.skip,
                                                limit=filters.limit,
                                                email = filters.email,
                                                order_id = filters.order_id,
                                                from_date = filters.from_date,
                                                to_date = filters.to_date,
                                                session=session)
    """All orders for Admin"""
    return all_orders


@router.get("/order/monthlysales")
async def get_order_monthly():
    """Total Sales by Month"""
    query = 'select created_at, total from order_data'
    df = get_dataframe(query=query)
    df.index = pd.to_datetime(df['created_at'])
    month_total = df.groupby(pd.Grouper(freq='M'))['total'].count()
    month_total.index = month_total.index.strftime('%B')

    return month_total.to_json()


@router.get("/order/dailysales")
async def get_order_daily():
    """Daily total orders last 30 days"""
    query = 'select created_at, order_id, total from order_data'
    df = get_dataframe(query=query)
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_month = df[df['created_at'] >= pd.to_datetime(
        'today')-pd.DateOffset(months=1)]

    day_total = last_month.groupby(last_month['created_at'].dt.date)[
        'total'].count()

    return day_total.to_json()


@router.get("/order/top_customers")
async def get_top_customers():
    """Top 10 Customers"""
    query = "select email, count(total) as total from order_data group by email order by total DESC limit 10"
    df = get_dataframe(query=query)
    return df.to_json(orient="records")


@router.get("/order/top_orders")
async def get_top_amount():
    """Top 10 highest orders"""
    query = 'select email, total from order_data order by total DESC limit 10'
    df = get_dataframe(query=query)
    return df.to_json(orient="records")


@router.get("/order/lastday")
async def get_daily_history():
    """Orders from the last 24 hrs"""
    limit = datetime.now() - timedelta(days=1)
    
    query = f"select * from order_data where created_at > '{limit}'"
    df = get_dataframe(query=query)

    df['created_at'] = pd.to_datetime(df['created_at'])
    last_day = df
    print(last_day)
    return last_day.to_json(orient="records")


@router.get("/order/{order_id}")
async def get_order_details(order_id=str, session: AsyncSession = Depends(getSession)):
    """queries order by id"""
    try:
        items = await AdminItemCrud.get_order_by_id(id=order_id, session=session)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/upload")
async def upload_file(file: UploadFile, session: AsyncSession = Depends(getSession)):
    """will read a csv and write to database new or existing items"""
    try:
        df = pd.read_csv(file.file)
        df.fillna('', inplace=True)
        df['price'] = df['price'].astype(float)
        df['in_stock'] = df['in_stock'].astype(int)
        df['barcode'] = df['barcode'].astype(str)
        items = df.to_dict(orient="records")

        await ItemCrud.items_from_import(items, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
