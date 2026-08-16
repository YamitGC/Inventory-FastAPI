# Product ORM Model

from sqlalchemy import Column, Float, Integer, String
from app.database import Base

class ProductTable(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    categoria = Column(String, index=True, nullable=False)
    precio = Column(Float, nullable=False)
    unidades = Column(Integer, default=0)
