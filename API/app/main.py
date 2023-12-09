import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .items import routes as ItemRoutes
from .orders import routes as OrderRoutes
from starlette_admin.contrib.sqla import Admin, ModelView

from .admin.views.sales_view import SalesView
from .models import Items, Order, OrderDetail, ItemsByOrder
from .db import engine

origins = [
    "http://localhost:5173"
]

app = FastAPI()

star_admin = Admin(engine, title="Admin Panel")
star_admin.add_view(ModelView(Items))
star_admin.add_view(OrderDetail(Order))
star_admin.add_view(ModelView(ItemsByOrder))
star_admin.mount_to(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ItemRoutes.router, prefix="/api")
app.include_router(OrderRoutes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}
