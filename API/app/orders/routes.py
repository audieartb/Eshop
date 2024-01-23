from app.db import getSession, cache
from app.models import OrderCreate
from app.orders.crud import OrderCrud
from app.items.crud import ItemCrud
import pickle
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..utils.email_utils import send_order_confirmation, send_order_history
from ..utils.token_utils import verify_token
from datetime import datetime

router = APIRouter()


@router.post("/orders", status_code=200, tags=['Orders'])
async def create_order(order: OrderCreate, session: AsyncSession = Depends(getSession), redis_client: cache = Depends(cache)):
    """Creates Order with status Pending"""
    try:
        if not order.items:
            # checks for empty basket
            return Response(status_code=400)
        out_of_stock = await ItemCrud.check_item_stock(items=order.items, session=session)
        if (out_of_stock):
            return JSONResponse(status_code=400, content=jsonable_encoder(out_of_stock))

        temp_id = OrderCrud.generate_order_id()
        order.temp_id = temp_id
        order.created_at = datetime.now()
        redis_client.set(f"order_{temp_id}", pickle.dumps(order))
        send_order_confirmation(email=order.email, order_id=order.temp_id)
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/orders/seed", tags=['Orders'])
async def seed_orders(orders: list[OrderCreate], session: AsyncSession = Depends(getSession)):
    for order in orders:
        try:

            if not order.items:
                return Response(status_code=400)
            out_of_stock = await ItemCrud.check_item_stock(items=order.items, session=session)
            if (out_of_stock):
                return JSONResponse(status_code=400, content=jsonable_encoder(out_of_stock))
            res = await OrderCrud.create_order(order=order, session=session)
            send_order_confirmation(email=res.email, order_id=res.order_id)
            return
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/orders/history", status_code=200, tags=['Orders'])
async def mail_order(email: str, session: AsyncSession = Depends(getSession)):
    """Finds all orders related to email and sends them"""
    try:
        res = await OrderCrud.find_order(email=email, session=session)

        orders_list = {x.id for x in res}
        public_ids = [{x.id :x.order_id} for x in res]
        items_list = await OrderCrud.get_items_order(orders_list=orders_list, session=session)

        await send_order_history(email=email, items_list=items_list)
        return
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/orders/confirmation", status_code=200, tags=['Orders'])
async def order_confirmation(token: str, session: AsyncSession = Depends(getSession), redis_client: cache = Depends(cache)):
    """Verifies token from user and changes status of order"""
    try:
        _data = verify_token(token=token)
        if (_data['check']):
            temp_id = _data['data']['order_id']
            email = _data['data']['email']

            if (cached_order := redis_client.get(f"order_{temp_id}",)) is not None:
                order = OrderCreate.from_orm(pickle.loads(cached_order))
                out_of_stock = await ItemCrud.update_sold_items(items=order.items, session=session)
                if (out_of_stock):
                    return JSONResponse(status_code=400, content=jsonable_encoder(out_of_stock))

                res = await OrderCrud.create_order(order=order, session=session)
                redis_client.delete(f"order_{temp_id}")

            return res
        else:
            raise HTTPException(
                status_code=400, detail='This link is no longer valid')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/orders/resend", tags=['Orders'])
async def resend_email(token: str, session: AsyncSession = Depends(getSession)):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
