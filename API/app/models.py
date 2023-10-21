from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


########### Items SQLModel ###########
class ItemsBase(SQLModel):
    """For Order Information on Emails"""
    item: str
    description: str
    price: float


class ItemsDetails(ItemsBase):
    """For details page and reporting"""
    barcode: str
    in_stock: int
    sold: int


class Items(ItemsDetails, table=True):
    """for database"""
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)


class ItemsCreate(ItemsDetails):
    """Model for Item creation"""
    pass


########### Orders SQLModel ###########
class OrderBase(SQLModel):
    """Order Details"""
    email: str
    created_at: datetime
    address: str
    transaction_id: str
    status: str
    total: float


class Order(OrderBase, table=True):
    """Order table for database"""
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    order_items: List["ItemsByOrder"] = Relationship(back_populates='order')


class OrderCreate(OrderBase):
    """Order creation must include at least 1 item"""
    items: List[Items]


########### OrderXItems SQLModel ###########
class ItemsByOrderBase(SQLModel):
    """Reference to Items and Orders"""
    order_id: Optional[int] = Field(default=None, foreign_key="order.id")
    item_id: Optional[int] = Field(default=None, foreign_key="items.id")


class ItemsByOrder(ItemsByOrderBase, table=True):
    """For database and Relationshiop with Orders table"""
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    order: Optional[Order] = Relationship(back_populates='order_items')


class ItemsByOrderCreate(ItemsByOrderBase):
    """Must Include existing Order and Items"""
    pass
