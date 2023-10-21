from fastapi import FastAPI
from app.routes import items
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.include_router(items.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}

