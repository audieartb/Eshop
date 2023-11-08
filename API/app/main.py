import uvicorn
from fastapi import FastAPI
from app.items import routes as ItemRoutes
from app.orders import routes as OrderRoutes
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.include_router(ItemRoutes.router, prefix="/api")
app.include_router(OrderRoutes.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}