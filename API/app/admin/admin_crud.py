from app.models import Item,Order,ItemOrderLink
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_, and_
from fastapi import HTTPException


class AdminItemCrud:

    @classmethod
    async def get_orders(cls):
        pass

    @classmethod
    async def get_items(cls):
        pass

    @classmethod
    async def get_order_by_id(cls, id: str, session: AsyncSession):

        checkdata = await session.exec(select(Order).where(Order.order_id == id))
        order = checkdata.first()
    
        if(order):
            result = await session.exec(select(Item.price, Item.title, Item.image, ItemOrderLink.qty).filter(and_(ItemOrderLink.order_id == order.id, ItemOrderLink.item_id == Item.id)))
            items = result.all()
            return items
        
    @classmethod
    async def get_order_monthly(cls):
        pass

    @classmethod
    async def get_order_daily(cls):
        pass

    @classmethod
    async def get_top_order(cls):
        pass

    @classmethod
    async def get_top_amoun(cls):
        pass

    @classmethod
    async def get_daily_history(cls):
        pass

    


