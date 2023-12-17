from ..models import Item, ItemDetails, ItemBase, ItemOrderLink, OrderItem
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_
from fastapi import HTTPException




class ItemCrud:
        
    @classmethod    
    async def get_items(cls, limit: int, skip: int, price_from: int | None,
                        price_to: int | None, search: str, session: AsyncSession):
        """Handles all queries to multiple items"""
        statement = select(Item).offset(skip).limit(limit)
        if search:
            statement = statement.filter(or_(
                Item.item.regexp_match(search, 'i'), Item.description.regexp_match(search, 'i')))

        if price_from:
            statement = statement.where(Item.price > price_from)
        if price_to:
            statement = statement.where(Item.price < price_to)

        result = await session.execute(statement)
        items = result.scalars().all()
        return items

    @classmethod 
    async def item_by_id(cls, barcode: str, session: AsyncSession):
        """finds item by barcode"""
        result = await session.execute(select(Item).where(Item.barcode == barcode))
        item = result.first()
        return item

    @classmethod
    async def add_item(cls, item: Item, session: AsyncSession):
        """adds single item to database"""
        db_item = Item.from_orm(item)
        session.add(db_item)
        await session.commit()
        await session.refresh(db_item)
        return db_item

    @classmethod
    async def update_item(cls, item: Item, session: AsyncSession):
        res = session.exec(select(Item).where(Item.id == item.id))
        db_item = res.one()
        if (not db_item):
            raise HTTPException(
                status_code=404, detail="Item does not exist in database")
        db_item = item
        session.add(db_item)
        session.commit()
        return db_item

    @classmethod
    async def update_item_sold(cls, item_id: int, sold: int, session: AsyncSession):
        """for every sold item updates the stock"""
        statement = select(Item).where(Item.id == item_id)
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

    @classmethod
    async def create_items(cls, items: list[ItemDetails], session: AsyncSession):
        """creates from a list of items"""
        for item in items:
            temp = Item.from_orm(item)
            session.add(temp)
        await session.commit()
        return
    
    @classmethod
    async def check_item_stock(cls, items: list[OrderItem], session: AsyncSession):
        """Retrives only items that have enough stock, Cancels all if one fails"""
        out_of_stock = []
        try:
            for item in items:
                result = await session.exec(select(Item).where(Item.barcode == item.barcode).where(Item.in_stock > item.qty))
                db_item = result.first()

                if db_item is None:
                    out_of_stock.append(item)
                    continue

                db_item.in_stock -= item.qty
                db_item.sold += item.qty
                session.add(db_item)

            if (out_of_stock):
                return out_of_stock
            await session.commit()
            return None

        except Exception as e:
            await session.rollback()
            raise e