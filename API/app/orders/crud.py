from datetime import date, datetime
import string
import random
from ..db import getSession
from ..models import Order, OrderCreate, OrderItem, ItemsByOrder
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


async def create_order(order: OrderCreate, session: AsyncSession) -> str:
    """creates new order"""
    order_id = generate_order_id()
    
    db_order = Order(
        order_id=order_id,
        email=order.email,
        address=order.address,
        transaction_id=order.transaction_id,
        status=order.status,
        total=order.total
    )
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)
    print(order.items)
    for item in order.items:
        temp = ItemsByOrder(order_id=db_order.id, item_id=item.barcode)
        print(temp)
        session.add(temp)
    await session.commit()
    return order_id


async def check_item_stock():
    pass


def create_item_by_order(order_id: string, order_items: list[OrderItem]):
    """creates relationship Items X Order"""
    for item in order_items:
        pass


def generate_order_id():
    """generates unique order id for user"""
    today = date.today()
    alph = string.ascii_uppercase + string.digits
    rand_string = ''.join(random.choice(alph) for i in range(7))
    return f"${today.day}${today.month}-${rand_string}"

