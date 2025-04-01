from datetime import datetime
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.model.dao import Order, OrderState, OrderItem
from app.model.dto import CreateOrderReqDto
from app.repository.order_item import create_order_items, delete_order_items
from app.repository.product import get_product


# TODO: put all method in injectable classes (as services)


def create_order(db: Session, 
                 order_request: CreateOrderReqDto) -> Order | None:
    """
    Create an Order entity and related OrderItem entities as described in a given creation request.
    """

    order = None
    try:
        with db.begin():
            created_at = datetime.now()
            order = Order(
                created_at = created_at,
                state = OrderState.CREATED,
                customer_email=order_request.customer_email,
                total_price=0.
            )
            db.add(order)
            db.flush()

            create_order_items(db, order_request, order)
            db.commit()
        
    except (SQLAlchemyError, ValueError) as e:
        db.rollback()
        raise e

    return order


def get_order(db: Session, 
              _id: Optional[int] = None,
              lock_row: Optional[bool] = False) -> Order | None:
    """
    Get an Order by its ID
    """

    query = db.query(Order)
    
    if _id:
        query = query.filter(Order.id == _id)
    if lock_row:
        query = query.with_for_update()
    
    order = query.first()
    return order


def get_orders(db: Session, 
               lock_row: Optional[bool] = False) -> list[Order]:
    """
    Read all Order entities.
    """

    query = db.query(Order)
    
    if lock_row:
        query = query.with_for_update()
    
    products = query.all()
    return products


def update_order(db: Session, 
                 order_id: int, 
                 order_request: CreateOrderReqDto) -> Order | None:
    """
    Update an Order entity given a request DTO.
    """

    order = None
    try:
        with db.begin():
            order = get_order(db, _id=order_id, lock_row=True)
            if order:
                delete_order_items(db, order_id)
                db.flush()
                create_order_items(db, order_request, order)
                order.state = OrderState.CHANGED

            db.commit()
        
    except (SQLAlchemyError, ValueError) as e:
        db.rollback()
        raise e

    return order


def delete_order(db: Session, 
                order_id: int = None) -> None:
    """
    Delete an Order entity given its ID.
    The quantities specified in the items are NOT rebalanced in the stocks.
    """

    try:
        with db.begin():
            delete_order_items(db, order_id, rebalance_stocks=False)
            query = db.query(Order).filter(Order.id == order_id)
            query.delete()

    except (SQLAlchemyError, ValueError) as e:
        db.rollback()
        raise e