from fastapi import FastAPI
from app.database import Base, engine
from app.routers.product import router as product_router

# Create the tables in the database if they do not exist.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management API",
    version="1.0"
)

app.include_router(product_router)

@app.get("/")
def root():
    return {"message": "Inventory API is running"}

