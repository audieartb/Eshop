from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .items import routes as ItemRoutes
from .orders import routes as OrderRoutes
from .admin import admin_routes as AdminRoutes
from .admin import user_routes as UserRoutes
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.views import BaseModelView
from .models import Item, Order, OrderDetail
from .db import engine



origins = [
    "http://localhost:5173"
]

app = FastAPI()

class ChartView(BaseModelView):
    pass

star_admin = Admin(engine, title="Admin Panel")
star_admin.add_view(ModelView(Item))
star_admin.add_view(OrderDetail(Order))

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(ItemRoutes.router, prefix="/api")
app.include_router(OrderRoutes.router, prefix="/api")
app.include_router(AdminRoutes.router, prefix="/admin")
app.include_router(UserRoutes.router, prefix="/admin" )

@app.get("/")
def read_root():
    return {"Hello": "World"}
