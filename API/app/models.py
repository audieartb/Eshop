from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from starlette_admin.contrib.sqla import ModelView
from dateutil.relativedelta import relativedelta

def test_date():
    return datetime.now() - relativedelta(months=11)

class AdminUserBase(SQLModel):
    username: str = Field(nullable=False, unique=True)
    last_login: datetime = Field(nullable=True)


class AdminUser(AdminUserBase, table=True):
    id: int = Field(primary_key=True, nullable=False)
    hashed_password: str = Field(nullable=False)

########### Item SQLModel ###########


class ItemBase(SQLModel):
    """For Order Information on Emails"""
    title: str
    description: str
    price: float
    barcode: str = Field(nullable=False, unique=True)
    image: str


class ItemDetails(ItemBase):
    """For details page, reporting and adding items to database"""
    sold: int
    in_stock: int


class Item(ItemDetails, table=True):
    """for database"""
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    item_order: Optional['ItemOrderLink'] = Relationship(
        back_populates='item_ref')
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class OrderItem(SQLModel):
    """Only for order creation"""
    barcode: str
    qty: int
    id: int
    price: float

########### Orders SQLModel ###########


class OrderBase(SQLModel):
    """Order Details"""
    email: str
    address: str
    status: str
    total: float
    delivery_type: str
   


class Order(OrderBase, table=True):
    """Order table for database"""
    __tablename__ = "order_data"
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    order_id: str = Field(nullable=False, unique=True)
    order_items: List["ItemOrderLink"] = Relationship(
        back_populates='order_ref', sa_relationship_kwargs={'lazy': 'selectin'})
    created_at: datetime = Field(default_factory=datetime.now)
    transaction_id: str = Field(default=None, nullable=False)


class OrderDetail(ModelView):
    fields = ['order_id', 'created_at',
              'transaction_id', 'email', 'status', 'total']


class OrderCreate(OrderBase):
    """Order creation must include at least 1 item"""
    temp_id : str = Field(default=None)
    items: List[OrderItem]

########### OrderXItem SQLModel ###########
class ItemOrderLink(SQLModel, table=True):
    __tablename__ = 'item_order_link'
    """For database and Relationshiop with Orders table"""
    id: Optional[int] = Field(default=None, nullable=False, primary_key=True)
    qty: int = Field(nullable=False)
    order_id: int = Field(foreign_key="order_data.id")
    item_id: int = Field(foreign_key="item.id")
    order_ref: Optional[Order] = Relationship(back_populates='order_items')
    item_ref: Optional[Item] = Relationship(
        back_populates='item_order', sa_relationship_kwargs={'lazy': 'selectin'})
    

class SearchFilters(SQLModel):
    order_by: str = 'created_at'
    order_asc: bool = False
    skip: int = 0
    limit: int | None
    email:str | None
    order_id: str | None
    from_date: str
    to_date: str