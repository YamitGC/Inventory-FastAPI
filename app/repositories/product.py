from sqlalchemy.orm import Session
from app.models import Product
from app.schemas.product import ProductCreate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db # Database session injection
        
    def create(self, product_data: ProductCreate) -> Product:
        # Pydantic schema -> SQLAlchemy model
        product_db = Product(**product_data.model_dump())
        # Persist to the database
        self.db.add(product_db)
        self.db.commit()
        self.db.refresh(product_db)  # Gets the ID assigned by SQLite
        return product_db
    
    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()