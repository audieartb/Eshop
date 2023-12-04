from datetime import date, datetime
import string
import random
from ..db import getSession
from ..models import Order, OrderCreate, OrderItem, ItemsByOrder, Items
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, join


async def create_order(order: OrderCreate, session: AsyncSession) -> str:
    """creates new order"""
    order_id = generate_order_id()
    transaction_id = 'xxx999xxx000-xxx000ddd'
    db_order = Order(
        email=order.email,
        address=order.address,
        order_id=order_id,
        transaction_id=transaction_id,
        status='pending',
        total=order.total
    )
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)
    print(order.items)
    for item in order.items:
        temp = ItemsByOrder(order_id=db_order.id, item_barcode=item.barcode, qty=item.qty)
        session.add(temp)
    await session.commit()
    return db_order


async def check_item_stock():
    pass

async def change_order_status(order_id: str, email:str, status: str, session: AsyncSession):

    stmt = select(Order).where(Order.order_id == order_id).where(Order.email == email)
    results = await session.exec(stmt)
    order = results.one()
    order.status = status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

async def get_items_order(orders_list: list[str], session: AsyncSession):
    """get items from order"""
    stmt2 = select(Order.id, ItemsByOrder.qty, ItemsByOrder.order_id, Items).select_from(join(ItemsByOrder, Items)).where(
        Order.id.in_(orders_list)).where(Order.id == ItemsByOrder.order_id).order_by(Order.id)

    stmt1 = select(Order.id, ItemsByOrder).where(
        ItemsByOrder.order_id.in_(orders_list)).where(Order.id == ItemsByOrder.order_id)
    # result = select(ItemsByOrder, Items).where(ItemsByOrder.order_id == order_id)
    #                             .where(ItemsByOrder.item_barcode == Items.barcode)
    result = await session.exec(stmt1)

    items = result.all()

    return items


def create_item_by_order(order_id: string, order_items: list[OrderItem]):
    """creates relationship Items X Order"""
    for item in order_items:
        pass


async def find_order(email: string, session: AsyncSession):
    statement = select(Order).where(Order.email == email)
    result = await session.scalars(statement)
    order = result.all()
    return order


def generate_order_id():
    """generates unique order id for user"""
    today = date.today()
    alph = string.ascii_uppercase + string.digits
    rand_string = ''.join(random.choice(alph) for i in range(7))
    return f"${today.day}${today.month}-${rand_string}"
