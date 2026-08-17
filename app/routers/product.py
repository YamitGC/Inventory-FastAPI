from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.repositories.product import ProductRepository
from app.services.product import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    # Inject the database session into the repository and service.
    repository = ProductRepository(db)
    return ProductService(repository)

@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_data: ProductCreate, service: ProductService = Depends(get_product_service)) -> ProductResponse:
    return service.create_product(product_data)

@router.get("/", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
def get_all_products(service: ProductService = Depends(get_product_service)) -> List[ProductResponse]:
    return service.get_all_products()


@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def get_product_by_id(product_id: int, service: ProductService = Depends(get_product_service)) -> ProductResponse:
    return service.get_product_by_id(product_id)


@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
def update_product(product_id: int, product_data: ProductUpdate, service: ProductService = Depends(get_product_service)) -> ProductResponse:
    return service.update_product(product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product( product_id: int, service: ProductService = Depends(get_product_service)):
    service.delete_product(product_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)