from app.db import getSession
from app.models import Order, ItemsByOrderBase
import app.orders.crud as crud
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status   



router = APIRouter()

@router.post("/orders")
async def place_order(order: Order, session: AsyncSession = Depends(getSession)):
    try:
        pass
        
    except Exception as e:
        raise HTTPException(status_code=500) from e

@router.post("/orders/details")
async def mail_order(data: str, session: AsyncSession = Depends(getSession)):
    pass