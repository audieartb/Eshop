from app.models import Item,Order,ItemOrderLink
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_
from fastapi import HTTPException


class AdminItemCrud:

    @classmethod
    async def get_orders(cls):
        pass

    @classmethod
    async def get_items(cls):
        pass

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

    


