from datetime import date, datetime
import string
import random
import json
from ..models import Order, OrderCreate, OrderItem, ItemOrderLink, Item
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, join
from sqlalchemy.orm import selectinload


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
        total=order.total,
        delivery_type=order.delivery_type
    )
    session.add(db_order)
    await session.commit()
    await session.refresh(db_order)
    for item in order.items:
        temp = ItemOrderLink(order_id=db_order.id,
                             item_id=item.id, qty=item.qty)
        session.add(temp)
    await session.commit()
    return db_order


async def change_order_status(order_id: str, email: str, status: str, session: AsyncSession):

    stmt = select(Order).where(Order.order_id ==
                               order_id).where(Order.email == email)
    results = await session.exec(stmt)
    order = results.one()
    order.status = status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


async def get_items_order(orders_list: list[str], session: AsyncSession):
    """get items from order"""
    stmt2 = select(ItemOrderLink.qty, ItemOrderLink.order_id, Item.price, Item.item).select_from(join(ItemOrderLink, Item)).where(
        Order.id.in_(orders_list)).where(Order.id == ItemOrderLink.order_id).order_by(Order.id)

    stmt1 = select(ItemOrderLink).select_from().where(
        ItemOrderLink.order_id.in_(orders_list)).where(Order.id == ItemOrderLink.order_id)
    # result = select(ItemOrderLink, Item).where(ItemOrderLink.order_id == order_id)
    #                             .where(ItemOrderLink.item_barcode == Item.barcode)

    stmt3 = select(ItemOrderLink).options(selectinload(ItemOrderLink.item_ref,
                                                       ItemOrderLink.order)).where(ItemOrderLink.order_id.in_(orders_list))

    result = await session.exec(stmt2)

    items = result.all()

    return items

async def updateDate(session: AsyncSession):
    stmt = select()
    pass


async def get_history(email: str, session: AsyncSession):

    stmt = select(Order.id, ItemOrderLink, )

    pass


def create_item_by_order(order_id: string, order_items: list[OrderItem]):
    """creates relationship Item X Order"""
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
