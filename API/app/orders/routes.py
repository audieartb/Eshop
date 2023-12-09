from app.db import getSession
from app.models import OrderCreate
import app.orders.crud as crud
import app.items.crud as ItemsCrud
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..utils.email_utils import send_order_confirmation, send_order_history
from ..utils.token_utils import verify_token

router = APIRouter()


@router.post("/orders")
async def place_order(order: OrderCreate, session: AsyncSession = Depends(getSession)):
    """Creates Order with status Pending"""
    try:

        if not order.items:
            return Response(status_code=400)
        out_of_stock = await ItemsCrud.check_item_stock(items=order.items, session=session)
        if (out_of_stock):
            return JSONResponse(status_code=400, content=jsonable_encoder(out_of_stock))
        res = await crud.create_order(order=order, session=session)
        send_order_confirmation(email=res.email, order_id=res.order_id)
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/orders/history", status_code=200)
async def mail_order(email: str, session: AsyncSession = Depends(getSession)):
    """Finds all orders related to email and sends them"""
    try:
        res = await crud.find_order(email=email, session=session)
        orders_list = {x.id for x in res}
        items_list = await crud.get_items_order(orders_list=orders_list, session=session)
        
        await send_order_history(email=email, items_list=items_list)
        return 
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
            raise HTTPException(
                status_code=400, detail='This link is no longer valid')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/orders/resend")
async def resend_email(token: str, session: AsyncSession = Depends(getSession)):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
