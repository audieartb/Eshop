from app.models import Item, Order, ItemOrderLink
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_, and_, desc
from fastapi import HTTPException
from sqlalchemy import func


class AdminItemCrud:

    @classmethod
    async def get_orders(cls, skip: int | None, limit: int | None,
                         order_by: str | None, email: str| None, order_id: str| None,
                         from_date: str| None, to_date: str| None,
                         session: AsyncSession, order_asc:  bool = False):
        stmt = select(Order).offset(skip).limit(limit)

        if order_by and order_asc:
            stmt = stmt.order_by(order_by)
        if email:
            stmt = stmt.where(Order.email == email)
        if order_id:
            stmt = stmt.where(Order.order_id == order_id)

        res = await session.exec(stmt)
        orders = res.all()

        return orders

    @classmethod
    async def get_order_count(cls, session: AsyncSession):
        res = await session.exec(select(func.count(Order.id)))
        return {"count": res.one()}

    @classmethod
    async def get_items(cls):
        pass

    @classmethod
    async def get_order_by_id(cls, id: str, session: AsyncSession):

        checkdata = await session.exec(select(Order).where(Order.order_id == id))
        order = checkdata.first()

        if (order):
            result = await session.exec(select(Item.price, Item.title, Item.image, ItemOrderLink.qty).filter(and_(ItemOrderLink.order_id == order.id, ItemOrderLink.item_id == Item.id)))
            items = result.all()
            return items

    @classmethod
    async def get_monthly_sales(cls,  session: AsyncSession):

        pass

    @classmethod
    async def get_order_daily(cls):
        pass

    @classmethod
    async def get_top_order(cls):
        pass

    @classmethod
    async def get_top_amount(cls):
        pass

    @classmethod
    async def get_daily_history(cls):
        pass