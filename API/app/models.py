from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
import uuid
from starlette_admin.contrib.sqla import ModelView


########### Items SQLModel ###########
class ItemsBase(SQLModel):
    """For Order Information on Emails"""
    items: str
    description: str
    price: float
    barcode: str = Field(nullable=False, unique=True)
    in_stock: int
   

class ItemsDetails(ItemsBase):
    """For details page, reporting and adding items to database"""
    sold: int


class Items(ItemsDetails, table=True):
    """for database"""
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    to_order: Optional['ItemsByOrder'] = Relationship(back_populates='item_ref')

    

class OrderItem(SQLModel):
    """Only for order creation"""
    barcode: str
    qty: int

########### Orders SQLModel ###########

class OrderBase(SQLModel):
    """Order Details"""
    email: str
    address: str
    status: str
    total: float
    

class Order(OrderBase, table=True):
    """Order table for database"""
    __tablename__ = "order_data"
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    order_id: str = Field(nullable=False, unique=True)
    order_items: List["ItemsByOrder"] = Relationship(back_populates='order', sa_relationship_kwargs={'lazy': 'selectin'})
    created_at: datetime = Field(default_factory = datetime.utcnow)
    transaction_id: str = Field(default=None, nullable=False)
 

class OrderDetail(ModelView):
    fields = ['order_id', 'created_at', 'transaction_id', 'email', 'status', 'total']

class OrderCreate(OrderBase):
    """Order creation must include at least 1 item"""
    items: List[OrderItem]
    delivery_type: str


########### OrderXItems SQLModel ###########
class ItemsByOrderBase(SQLModel):
    """Reference to Items and Orders"""
    order_id: Optional[int] = Field(default=None, foreign_key="order_data.id")
    item_barcode: Optional[str] = Field(default=None, foreign_key="items.barcode")
    qty: int = Field(nullable=True)


class ItemsByOrder(ItemsByOrderBase, table=True):
    """For database and Relationshiop with Orders table"""
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    order: Optional[Order] = Relationship(back_populates='order_items')
    item_ref : Optional[Items] = Relationship(back_populates='to_order', sa_relationship_kwargs={'lazy': 'selectin'})

class ItemsByOrderCreate(ItemsByOrderBase):
    """Must Include existing Order and Items"""
    pass