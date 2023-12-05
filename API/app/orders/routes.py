from app.db import getSession
from app.models import OrderCreate
import app.orders.crud as crud
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException
from ..utils.email_utils import send_order_confirmation
from ..utils.token_utils import verify_token


router = APIRouter()


@router.post("/orders")
async def place_order(order: OrderCreate, session: AsyncSession = Depends(getSession)):
    """Creates Order with status Pending"""
    try:
      
        res = await crud.create_order(order=order, session=session)
        send_order_confirmation(email=res.email, order_id=res.order_id)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/orders/details")
async def mail_order(email: str, session: AsyncSession = Depends(getSession)):
    """Finds all orders related to email and sends them"""
    try:
        res = await crud.find_order(email=email, session=session)
        orders_list = {x.id for x in res}
        items_list = await crud.get_items_order(orders_list=orders_list, session=session)

        return items_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/orders/confirmation", status_code=200)
async def order_confirmation(token: str, session: AsyncSession = Depends(getSession)):
    """Verifies token from user and changes status of order"""
    try:
        _data = verify_token(token=token)
        if (_data['check']):
            res = await crud.change_order_status(
                order_id=_data['data']['order_id'], email=_data['data']['email'],  status='in_progress', session=session)
            return res
        else:
            raise HTTPException(status_code=400, detail='This link is no longer valid')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/orders/resend")
async def resend_email(token: str, session: AsyncSession = Depends(getSession)):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e