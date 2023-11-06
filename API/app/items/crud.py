from ..db import getSession
from ..models import Items, ItemsCreate, ItemsDetails
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class ItemCrud():

    @staticmethod
    async def get_items(limit: int, skip: int, session: AsyncSession):
        statement = select(Items).offset(skip).limit(limit)
        result = await session.execute(statement)
        items = result.scalars().all()
        return items

    @staticmethod
    async def item_by_id(barcode: str, session: AsyncSession):
        """finds item by barcode"""
        result = await session.execute(select(Items).where(Items.barcode == barcode))
        item = result.first()
        return item

    @staticmethod
    async def search_items(keyword: str, session: AsyncSession):
        """finds items based on keyword"""
        pass

    @staticmethod
    async def add_item(item: ItemsCreate, session: AsyncSession):
        db_item = Items.from_orm(item)
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item

    @staticmethod
    async def update_item_sold(item_id: int, sold: int, session: AsyncSession):
        statement = select(Items).where(Items.id == item_id)
        result = session.exe(statement)
        item = result.first()
        if (item is None):
            raise ValueError("Item does not exists")
        item.in_stock -= sold
        item.sold += sold

        session.add(item)
        session.commit()
        session.refresh(item)
        return item
