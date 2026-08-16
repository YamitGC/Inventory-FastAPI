from fastapi import FastAPI
from app.database import Base, engine
import app.models.product

Base.metadata.create_all(bind=engine)

app = FastAPI()