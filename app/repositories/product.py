from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import Product
from app.schemas.product import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db # Database session injection
        
    def create(self, product_data: ProductCreate) -> Product:
        # Pydantic schema -> SQLAlchemy model
        db_product = Product(**product_data.model_dump())
        # Persist to the database
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)  # Gets the ID assigned by SQLite
        return db_product
    
    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()
    
    def get_all(self) -> List[Product]:
        return self.db.query(Product).all()
    
    def update(self, product_id: int, product_data: ProductUpdate) -> Optional[Product]:
        db_product = self.get_by_id(product_id)
        if not db_product:
            return None
        
        # Filter only the fields submitted by the user (exclude None values)
        update_data = product_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
                setattr(db_product, key, value)
            
        self.db.commit()
        self.db.refresh(db_product)
        return db_product
    
    def delete(self, product_id: int) -> bool:
        db_product = self.get_by_id(product_id)
        if not db_product:
            return False
        
        self.db.delete(db_product)
        self.db.commit()
        return True