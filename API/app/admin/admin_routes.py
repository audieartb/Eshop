from fastapi import Depends, HTTPException, APIRouter, UploadFile, File, Form, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Annotated
import pandas as pd
from .admin_crud import AdminItemCrud
from app.db import PDENGINE
from app.db import getSession
import os
from datetime import datetime, timedelta
from app.models import ItemBase, ItemDetails
from app.items.crud import ItemCrud

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


def get_dataframe(query: str = '', filename: str = ''):

    query = "SELECT * from order_data"
    filename = "orders"

    if not check_file_exists(filename='orders'):
        df = pd.read_sql(query, con=PDENGINE)
        df.to_csv(path_or_buf=f'db_files/{filename}.csv')
        return df

    ctime = os.path.getctime(f'db_files/{filename}.csv')
    ctimestamp = datetime.fromtimestamp(ctime)
    if ((ctimestamp + timedelta(days=60)) > datetime.now()):
        df = pd.read_csv(f'db_files/{filename}.csv')
        return df
    else:
        df = pd.read_sql(query, con=PDENGINE)
        df.to_csv(path_or_buf=f'db_files/{filename}.csv')
        return df

@router.get("/item/count")
async def item_count(session: AsyncSession = Depends(getSession)):
    return await ItemCrud.item_count(session=session)

@router.get("/order")
async def get_orders():
    """All orders for Admin"""
    df = get_dataframe()
    orders = df.head(10)
    return orders.to_json(orient="records")


@router.get("/order/monthlysales")
async def get_order_monthly():
    """Total Sales by Month"""

    df = get_dataframe()

    df.index = pd.to_datetime(df['created_at'])
    month_total = df.groupby(pd.Grouper(freq='M'))['total'].count()
    month_total.index = month_total.index.strftime('%B')

    return month_total.to_json()


@router.get("/order/dailysales")
async def get_order_daily():
    """Daily total orders last 30 days"""

    df = get_dataframe()

    df['created_at'] = pd.to_datetime(df['created_at'])
    last_month = df[df['created_at'] >= pd.to_datetime(
        'today')-pd.DateOffset(months=1)]

    day_total = last_month.groupby(last_month['created_at'].dt.date)[
        'total'].count()

    return day_total.to_json()


@router.get("/order/top_customers")
async def get_top_order():
    """Top 10 Customers"""

    df = get_dataframe()

    by_email = df.groupby(df['email'])['total'].count(
    ).sort_values(ascending=False).head(10)

    return by_email.to_json()


@router.get("/order/top_orders")
async def get_top_amoun():
    """Top 10 highest orders"""

    df = get_dataframe()
    rank = df.sort_values(by=['total'], ascending=False).head(10)

    return rank.to_json(orient="records")


@router.get("/order/lastday")
async def get_daily_history():
    """Orders from the last 24 hrs"""

    df = get_dataframe()

    df['created_at'] = pd.to_datetime(df['created_at'])
    last_day = df[df['created_at'] >= (
        pd.to_datetime('today')-pd.Timedelta(days=1))]
    return last_day.to_json(orient="records")


@router.get("/order/{order_id}")
async def get_order_details(order_id=str, session: AsyncSession = Depends(getSession)):
    try:
        items = await AdminItemCrud.get_order_by_id(id=order_id, session=session)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/upload")
async def upload_file(file: UploadFile, session: AsyncSession = Depends(getSession)):

    try:
        df = pd.read_csv(file.file)
        print(df.head())
        df.fillna('', inplace=True)
        df['price'] = df['price'].astype(float)
        df['in_stock'] = df['in_stock'].astype(int)
        df['barcode'] = df['barcode'].astype(str)
        items = df.to_dict(orient="records")

        await ItemCrud.items_from_import(items, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e