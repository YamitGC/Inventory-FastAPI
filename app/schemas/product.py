from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

# 1. Base Schema (Common shared attributes)
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(..., min_length=2, max_length=50)
    price: float = Field(..., gt=0)  
    stock: int = Field(default=0, ge=0)

# 2. Create Schema (Input DTO for POST/PUT)
class ProductCreate(ProductBase):
    pass # Inherits all fields and validations from ProductBase

# 3. Response Schema (Output DTO for GET/Responses)
class ProductResponse(ProductBase):
    id: int # Database auto-incremented primary key
    
    class Config:
        model_config = ConfigDict(from_attributes=True) # Allows ORM model instance -> Pydantic model conversion
    