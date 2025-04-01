from typing import Optional
from sqlalchemy import update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.model.dao import OrderItem, Product
from app.model.dto import ProductDto


# TODO: put all method in injectable classes (as services)


def create_product(db: Session,
                   dto: ProductDto) -> Product | None:
    """
    Create a Product entity from DTO
    """

    product = Product(
        seller_email = dto.seller_email,
        name = dto.name,
        description = dto.description,
        manufacturer = dto.manufacturer,
        stocked_at = dto.stocked_at,
        price = dto.price,
        stock = dto.stock

    )
    db.add(product)
    db.commit()
    return product


def get_product(db: Session, 
                 _id: Optional[int] = None,
                 lock_row: Optional[bool] = False) -> Product | None:
    """
    Create a Product entity from ID
    """
    
    query = db.query(Product)
    
    if _id:
        query = query.filter(Product.id == _id)
    if lock_row:
        query = query.with_for_update()
    
    product = query.first()
    return product


def get_products(db: Session, 
                 _ids: Optional[list[int]] = None,
                 lock_row: Optional[bool] = False) -> list[Product]:
    """
    Read all Product entities
    """

    query = db.query(Product)
    
    if _ids:
        query = query.filter(Product.id.in_(_ids))
    if lock_row:
        query = query.with_for_update()
    
    products = query.all()
    return products


def unlink_product_items(db: Session,
                         product_id: Optional[int] = None) -> None:
    """
    Remove the link between an item and a deleted product.
    The item will remain with empty product_id.
    The unlinked item will still have some descriptive values of the product (when the order was created).
    """

    db.execute(
        update(OrderItem)
        .where(OrderItem.product_id == product_id)
        .values(product_id=None)
    )


def delete_product(db: Session, 
                   product_id: int = None) -> None:
    """
    Delete a Product entity.
    The related items will NOT be deleted, but unlinked from it.
    """

    try:
        with db.begin():
            unlink_product_items(db, product_id)
            query = db.query(Product).filter(Product.id == product_id)
            query.delete()
            db.commit()
        
    except (SQLAlchemyError, ValueError) as e:
        db.rollback()
        raise e