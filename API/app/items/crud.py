from ..db import getSession
from ..models import Items, ItemsDetails, ItemsBase
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_


async def get_items(limit: int, skip: int, price_from: int | None,
                    price_to: int | None, search: str, session: AsyncSession):
    """Handles all queries to multiple items"""
    statement = select(Items).offset(skip).limit(limit)
    if search:
        print('adds filter to ' + search)
        statement = statement.filter(or_(
            Items.item.regexp_match(search, 'i'), Items.description.regexp_match(search, 'i')))

    if price_from:
        statement = statement.where(Items.price > price_from)
    if price_to:
        statement = statement.where(Items.price < price_to)

    result = await session.execute(statement)
    items = result.scalars().all()
    return items


async def item_by_id(barcode: str, session: AsyncSession):
    """finds item by barcode"""
    result = await session.execute(select(Items).where(Items.barcode == barcode))
    item = result.first()
    return item


async def search_items(keyword: str, session: AsyncSession):
    """finds items based on keyword"""
    pass


async def add_item(item: Items, session: AsyncSession):
    db_item = Items.from_orm(item)
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    return db_item


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


async def create_items(items: list[Items], session: AsyncSession):
    for item in items:
        temp = Items.from_orm(item)
        session.add(temp)
    await session.commit()
    return
