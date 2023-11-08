from app.db import getSession
from app.models import Order, ItemsByOrderBase, OrderCreate
import app.orders.crud as crud
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status   



router = APIRouter()

@router.post("/orders")
async def place_order(order: OrderCreate, session: AsyncSession = Depends(getSession)):
    try:
        print(order)
        res = await crud.create_order(order=order, session=session)
        return res
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.get("/orders/details")
async def mail_order(data: str, session: AsyncSession = Depends(getSession)):
    pass
