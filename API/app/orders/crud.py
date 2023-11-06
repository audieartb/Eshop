from datetime import date
import string
import random
from ..db import getSession
from ..models import Order,OrderCreate, OrderItem
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


async def create_order(order:OrderCreate, session: AsyncSession):
    
    order_id = generateOrderId()

    for item in order.items:
        pass

    new_order = Order(
        email=order.email,
        created_at = order.created_at,
        address= order.address,
        transaction_id = order.transaction_id,
        status = 'pending',
        total = order.total,
        order_id = order_id,
    )
    
def createItemByOder(order_id:string, order_items: list[OrderItem]):

    for i in range(len(order_items)):
        pass



def generateOrderId():
    today = date.today()
    alph = string.ascii_uppercase + string.digits
    rand_string = ''.join(random.choice(alph) for i in range(7))
    return f"${today.day}${today.month}-${rand_string}"


async def delete():
    return False
