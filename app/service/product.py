from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.model.dto import ProductDto
import app.repository.product as product_repo



class ProductService:
    """
    Class for CRUD service on Product resource.
    """

    def __init__(self, db: Session = Depends(get_db),):
        self.db = db
        
    def create(self, product: ProductDto) -> int:
        new_product = product_repo.create_product(self.db, product)
        return new_product.id