from datetime import date
import string
import random
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, join
from ..models import Order, OrderCreate, ItemOrderLink, Item

class OrderCrud:

    @classmethod
    def generate_order_id(cls):
        """generates unique order id for user"""
        today = date.today()
        alph = string.ascii_uppercase + string.digits
        rand_string = ''.join(random.choice(alph) for i in range(7))
        return f"#{today.day}-{today.month}-${rand_string}"

    @classmethod
    async def create_order(cls, order: OrderCreate, session: AsyncSession) -> str:
        """creates new order"""
        transaction_id = 'xxx999xxx000-xxx000ddd'
        db_order = Order(
            email=order.email,
            address=order.address,
            order_id=order.temp_id,
            transaction_id=transaction_id,
            status='processing',
            total= sum(item.price * item.qty for item in order.items),
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
    
    @classmethod
    async def change_order_status(cls, order_id: str, email: str, status: str, session: AsyncSession):
        """Updates the order status pendin > in progress"""
        stmt = select(Order).where(Order.order_id ==
                                order_id).where(Order.email == email)
        results = await session.exec(stmt)
        order = results.one()
        order.status = status
        session.add(order)
        session.commit()
        session.refresh(order)
        return order

    @classmethod
    async def get_items_order(cls, orders_list: list[str], session: AsyncSession):
        """get items from order"""
        stmt = select(ItemOrderLink.qty, ItemOrderLink.order_id, Item.price, Item.title).select_from(join(ItemOrderLink, Item)).where(
            Order.id.in_(orders_list)).where(Order.id == ItemOrderLink.order_id).order_by(Order.id)

        result = await session.exec(stmt)
        items = result.all()
        return items
    
    @classmethod
    async def find_order(cls, email: string, session: AsyncSession):
        statement = select(Order).where(Order.email == email)
        result = await session.scalars(statement)
        order = result.all()
        return order
    
    @classmethod
    async def cancel_order(cls, order_id : str, session :AsyncSession):
        result  = await session.exec(select(Order).where(Order.order_id == order_id))
        order  = result.one()
        order.status = 'cancelled'

