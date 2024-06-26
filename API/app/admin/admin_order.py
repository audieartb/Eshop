from fastapi import Depends, HTTPException, APIRouter
from sqlmodel.ext.asyncio.session import AsyncSession
from dateutil.relativedelta import relativedelta
import pandas as pd
from .admin_crud import AdminCrud
from app.db import PDENGINE
from app.db import getSession
import os
from datetime import datetime, timedelta
from app.models import SearchFilters
from ..utils.email_utils import send_order_report

router = APIRouter()

def check_file_exists(filename: str):
    """For development only, to avoid querying database"""
    if not os.path.exists('db_files'):
        os.makedirs('db_files')

    if not os.path.exists(f'db_files/{filename}.csv'):
        with open(f'db_files/{filename}.csv', 'w+'):
            pass
        return False
    else:
        return True


def get_dataframe(query: str = None, filename: str = ''):
    """Currently configured for development, checks on local data"""
    query_all = 'select * from order_data'
    filename = "orders"

    if not check_file_exists(filename='orders'):
        df = pd.read_sql(query_all, con=PDENGINE)
        df.to_csv(path_or_buf=f'db_files/{filename}.csv')
        return df

    return pd.read_sql(query, con=PDENGINE)
    # ctime = os.path.getctime(f'db_files/{filename}.csv')
    # ctimestamp = datetime.fromtimestamp(ctime)
    # if ((ctimestamp + timedelta(seconds=1)) > datetime.now()):
    #     df = pd.read_csv(f'db_files/{filename}.csv')
    #     return df
    # else:
    #     df = pd.read_sql(query, con=PDENGINE)
    #     df.to_csv(path_or_buf=f'db_files/{filename}.csv')
    #     return df

@router.get("/order/count", tags=['Orders Admin'])
async def order_count(session: AsyncSession = Depends(getSession)):
    """Returns Total Count of Orders to calculate total pages"""
    return await AdminCrud.get_order_count(session=session)


@router.post("/order", tags=['Orders Admin'])
async def get_orders(filters: SearchFilters, session: AsyncSession = Depends(getSession)):
    """Gets orders for Admin and applies filters and pagination"""
    return await AdminCrud.get_orders(order_by=filters.order_by,
                                                order_asc=filters.order_asc,
                                                skip=filters.skip,
                                                limit=filters.limit,
                                                email=filters.email,
                                                order_id=filters.order_id,
                                                from_date=filters.from_date,
                                                to_date=filters.to_date,
                                                session=session)
    
@router.get("/order/monthlysales", tags=['Orders Admin'])
async def get_order_monthly():
    """Total Sales by Month"""
    date_limit = datetime.now() - relativedelta(months=12)
    query = f"select created_at, total from order_data where created_at > '{date_limit}'"
    df = get_dataframe(query=query)
    df.index = pd.to_datetime(df['created_at'])
    month_total = df.groupby(pd.Grouper(freq='M'))['total'].count()
    month_total.index = month_total.index.strftime('%B-%Y')

    return month_total.to_json()


@router.get("/order/dailysales", tags=['Orders Admin'])
async def get_order_daily():
    """Daily total orders in the last 30 days"""
    query = 'select created_at, order_id, total from order_data'
    df = get_dataframe(query=query)
    df['created_at'] = pd.to_datetime(df['created_at'])
    last_month = df[df['created_at'] >= pd.to_datetime(
        'today')-pd.DateOffset(months=1)]

    day_total = last_month.groupby(last_month['created_at'].dt.date)[
        'total'].count()

    return day_total.to_json()


@router.get("/order/top_customers", tags=['Orders Admin'])
async def get_top_customers():
    """Top 10 Customers"""
    query = "SELECT email, count(order_id) as total from order_data group by email order by total DESC limit 10"
    df = get_dataframe(query=query)
    return df.to_json(orient="records")


@router.get("/order/top_orders", tags=['Orders Admin'])
async def get_top_amount():
    """Top 10 highest amount orders"""
    query = 'select order_id, email, total from order_data order by total DESC limit 10'
    df = get_dataframe(query=query)
    return df.to_json(orient="records")


@router.get("/order/lastday", tags=['Orders Admin'])
async def get_daily_history():
    """Orders from the last 24 hrs"""
    limit = datetime.now() - timedelta(days=1)

    query = f"select * from order_data where created_at > '{limit}'"
    df = get_dataframe(query=query)

    df['created_at'] = pd.to_datetime(df['created_at'])
    last_day = df
    print(last_day)
    return last_day.to_json(orient="records")


@router.get("/order/{order_id}", tags=['Orders Admin'])
async def get_order_details(order_id=str, session: AsyncSession = Depends(getSession)):
    """queries order by id and returns details"""
    try:
        
        items = await AdminCrud.get_order_by_id(order_id=order_id, session=session)
        return items
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/order/daily/popular", tags=['Orders Admin'])
async def low_stock():
    """Returns items with low stock"""
    try:
        query = "select title, in_stock from item where in_stock < 20 order by in_stock limit 10"
        df = get_dataframe(query=query)
        return df.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(
            status_code=500, detail='Error generating report. '+str(e)) from e


@router.post("/order/report/{email}/{file_type}", tags=['Orders Admin'])
async def send_report(email: str, file_type: str):
    """Generates all orders report for admin and sends via email"""
    try:
        query = "select * from order_data limit 5"
        df = get_dataframe(query=query)
        send_order_report(df=df, file_type=file_type, email=email)

    except Exception as e:
        raise HTTPException(
            status_code=500, detail='Error generating report. '+str(e)) from e