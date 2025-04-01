from typing import Optional
from sqlalchemy.orm import Session

from app.model.dao import Order, OrderItem
from app.model.dto import CreateOrderReqDto
from app.repository.product import get_product, get_products


# TODO: put all method in injectable classes (as services)


def get_order_item(db: Session, 
                    order_id: Optional[int] = None,
                    product_id: Optional[int] = None,
                    lock_row: Optional[bool] = False) -> Order | None:
    """
    Create on OrderItem entity given some Order + Product IDs for the item.
    """

    query = db.query(OrderItem)
    
    if order_id:
        query = query.filter(OrderItem.order_id == order_id)
    if product_id:
        query = query.filter(OrderItem.product_id == product_id)
    if lock_row:
        query = query.with_for_update()
    
    order = query.first()
    return order



def create_order_items(db: Session, 
                       order_request: CreateOrderReqDto, 
                       order: Order) -> None:
    """
    Create the OrderItem entities for an empty order, as described by its creation request.
    """

    total_price = 0
    for p in order_request.items:
        product = get_product(db, _id=p.product_id, lock_row=True)
        if not product:
            raise ValueError(f"Product {p.product_id} not found")
        if product.stock < p.quantity:
            raise ValueError(f"Not enough stock for product {p.product_id}")
        
        product.stock -= p.quantity
        order_item = OrderItem(
            order_id=order.id, 
            product_id=product.id,
            product_name=product.name,
            product_description=product.description,
            product_price=product.price,
            quantity=p.quantity
        )
        db.add(order_item)
        
        total_price += product.price * p.quantity

    order.total_price = total_price
    db.flush()
    db.refresh(order, attribute_names=['items'])


def delete_order_items(db: Session, 
                        order_id: int = None,
                        rebalance_stocks: bool = True) -> None:
    """
    Delete the OrderItem entities related to a given order ID, by optionally rebalancing the product stocks.
    """

    query = db.query(OrderItem).filter(OrderItem.order_id == order_id)
    if rebalance_stocks:
        items = query.all()
        for i in items:
            product = get_product(db, i.product_id, lock_row=True)
            if product:
                product.stock += i.quantity
            #db.refresh(product)
    query.delete()