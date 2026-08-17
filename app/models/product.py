# Product ORM Model

from sqlalchemy import Column, Float, Integer, String
from app.database import Base

class ProductTable(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String, index=True, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
