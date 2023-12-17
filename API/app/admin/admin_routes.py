from fastapi import FastAPI, Depends, HTTPException, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession
import numpy as np
import pandas as pd
from .admin_crud import AdminItemCrud
from app.db import PDENGINE
import os
from datetime import datetime, timedelta
import csv

router = APIRouter()


def check_file_exists(filename: str):
    if not os.path.exists('db_files'):
        os.makedirs('db_files')

    if not os.path.exists(f'db_files/{filename}.csv'):
        with open(f'db_files/{filename}.csv', 'w+'): pass
        return False
    else:
        return True


def get_dataframe(query:str, filename: str):

    if not check_file_exists(filename='orders'):
        df = pd.read_sql(query, con=PDENGINE)
        df.to_csv(path_or_buf=f'db_files/{filename}.csv')
        print("fresh data",df)
        return df

    ctime = os.path.getctime(f'db_files/{filename}.csv')
    ctimestamp = datetime.fromtimestamp(ctime)
    if((ctimestamp + timedelta(minutes=60)) > datetime.now() ):
        print('from csv')
        df = pd.read_csv(f'db_files/{filename}.csv')
        return df
    else:
        print('from db')
        df = pd.read_sql(query, con=PDENGINE)
        df.to_csv(path_or_buf=f'db_files/{filename}.csv')
        return df

@router.post("/login")
async def login():
    pass



@router.get("/order")
async def get_orders():
    pass



@router.get("/items")
async def get_items():
    pass

@router.get("/order/monthly")
async def get_order_monthly():
        
    query = "SELECT * from order_data"
    file = "orders"
    df =  get_dataframe(query=query, filename=file)

    df.index = pd.to_datetime(df['created_at'])
    month_total = df.groupby(pd.Grouper(freq='M'))['total'].count()
    month_total.index = month_total.index.strftime('%B')
    print(month_total)
    return month_total.to_json()

@router.get("/order/daily")
async def get_order_daily():
    query = "SELECT * from order_data"
    file = "orders"
    df =  get_dataframe(query=query, filename=file)

    df['created_at'] = pd.to_datetime(df['created_at'])
    last_month = df[df['created_at']>= pd.to_datetime('today')-pd.DateOffset(months=1)]

    day_total = last_month.groupby(last_month['created_at'].dt.date)['total'].count()
    print(day_total)
    return day_total.to_json()

@router.get("/order/ordersbyemail")
async def get_top_order():
    query = "SELECT * from order_data"
    file = "orders"
    df =  get_dataframe(query=query, filename=file)

    by_email = df.groupby(df['email'])['total'].count().sort_values(ascending=False).head(10)
    print(by_email)
    return by_email.to_json()

@router.get("/order/amount")
async def get_top_amoun():
    query = "SELECT * from order_data"
    file = "orders"
    df =  get_dataframe(query=query, filename=file)
    rank = df.sort_values(by=['total']).head(10)

    return  rank.to_json()
@router.get("/order/history")
async def get_daily_history():
    query = "SELECT * from order_data"
    file = "orders"
    df =  get_dataframe(query=query, filename=file)
    
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_day = df[df['created_at']>= (pd.to_datetime('today')-pd.Timedelta(days=1))]
    return last_day.to_json()


