from fastapi import HTTPException, status
from typing import List
from app.repositories.product import ProductRepository
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import ProductTable

class ProductService:
    # Connection between the service and the database using dependency injection.
    def __init__(self, repository: ProductRepository):
        self.repository = repository
        
    def create_product(self, product_data: ProductCreate) -> ProductTable:
        return self.repository.create(product_data)
        
    def get_product_by_id(self, product_id: int) -> ProductTable:
        product = self.repository.get_by_id(product_id)
        if product is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found")
        return product
    
    def get_all_products(self) -> List[ProductTable]:
        return self.repository.get_all()
    
    def update_product(self, product_id: int, product_data: ProductUpdate) -> ProductTable:
        product = self.repository.update(product_id, product_data)
        if product is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found")
        return product
    
    def delete_product(self, product_id) -> None:
        product = self.repository.delete(product_id)
        if not product:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product not found")
        