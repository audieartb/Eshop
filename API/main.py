from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.items import routes as ItemRoutes
from app.orders import routes as OrderRoutes
from app.admin import order_routes as AdminOrderRoutes
from app.admin import item_routes as AdminItemRoutes
from app.admin import user_routes as UserRoutes
from starlette_admin.contrib.sqla import Admin, ModelView
from starlette_admin.views import BaseModelView
from app.models import Item, Order, OrderDetail
from app.db import engine



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
app.include_router(AdminOrderRoutes.router, prefix="/admin")
app.include_router(AdminItemRoutes.router, prefix="/admin")
app.include_router(UserRoutes.router, prefix="/admin" )

@app.get("/")
def read_root():
    return {"Hello": "World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)