from ..models import Item, ItemDetails, ItemBase, ItemOrderLink, OrderItem
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import func


class ItemCrud:

    @classmethod
    async def get_items(cls, limit: int, skip: int, price_from: int | None,
                        price_to: int | None, search: str, session: AsyncSession):
        """Handles all queries to multiple items"""
        statement = select(Item).offset(skip).limit(limit)
        if search:
            statement = statement.filter(or_(
                Item.title.regexp_match(search, 'i'), Item.description.regexp_match(search, 'i')))
        if price_from:
            statement = statement.where(Item.price > price_from)
        if price_to:
            statement = statement.where(Item.price < price_to)

        result = await session.execute(statement)
        items = result.scalars().all()
        return items
    
    @classmethod
    async def item_count(cls, session: AsyncSession):
        res = await session.exec(select(func.count(Item.id)))
        return {"count": res.one()}
        


    @classmethod
    async def item_by_id(cls, barcode: str, session: AsyncSession):
        """finds item by barcode"""
        result = await session.execute(select(Item).where(Item.barcode == barcode))
        item = result.first()
        return item

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
        await session.commit()
        await session.refresh(item)
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
    async def items_from_import(cls, items_list: list, session: AsyncSession):
        try:
            updated_at = datetime.now()
            print(items_list)
            for item in items_list:
                result = await session.exec(select(Item).where(Item.barcode == item['barcode']))
                db_item = result.one_or_none()
                if not db_item:
                    new_prod = Item(title=item["title"], description=item['description'],
                                    price=item['price'], barcode=item["barcode"], image='',
                                    in_stock=item['in_stock'], sold=0)

                    session.add(new_prod)
                    continue
                db_item.in_stock += item['in_stock']
                db_item.updated_at = updated_at
                session.add(db_item)
            await session.commit()
            return
        except Exception as e:
            raise e
        finally:
            await session.close()

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
                db_item.updated_at = datetime.now()
                session.add(db_item)

            if (out_of_stock):
                return out_of_stock
            await session.commit()
            return None

        except Exception as e:
            await session.rollback()
            raise e
