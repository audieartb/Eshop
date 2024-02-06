from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from app.items import routes as ItemRoutes
from app.orders import routes as OrderRoutes
from app.admin import admin_order as AdminOrderRoutes
from app.admin import admin_item as AdminItemRoutes
from app.admin import admin_user as UserRoutes


origins = [
    "http://localhost:5173"
]

app = FastAPI()

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