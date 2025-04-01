from app.model.dao import Order
from app.model.dto import OrderDto, OrderDto2, OrderItemDto, OrderItemDto2


def orders_dto_from_dict(orders: list[dict]) -> list[OrderDto]:
    """
    Methods for converting some order in dict-form to corresponding DTO
    """
    output = []
    for o in orders:
        items = []
        for i in o['items']:
            ii = OrderItemDto(**i)
            items.append(ii)
        o = o.copy()
        o['items'] = items
        oo = OrderDto(**o)
        output.append(oo)
    return orders

def order_to_dto2(order: Order) -> OrderDto2:
    """
    Method for converting a given order to corresponding DTO2 (for meili)
    """
    if order.items:
        order_items = [
            OrderItemDto2(
                # order_id=e.order_id,
                product_id=e.product_id,
                product_name=e.product_name,
                product_description=e.product_description,
                product_price=e.product_price,
                quantity=e.quantity
            ) for e in order.items
        ]
    else:
        order_items = []
    closed_at = None
    if order.closed_at:
        closed_at = str(order.closed_at)
    order_dto = OrderDto2(
        id=order.id,
        created_at=str(order.created_at), closed_at=closed_at,
        customer_email=order.customer_email,
        total_price=order.total_price, state=str(order.state),
        items=order_items
    )
    return order_dto

def orders_to_dto(orders: list[Order]) -> list[OrderDto]:
    """
    Methods for converting some orders DAOs to corresponding DTOs
    """
    output = []
    for o in orders:
        items = []
        for i in o.items:
            item = OrderItemDto(
                order_id=i.order_id, 
                product_id=i.product_id, 
                product_name=i.product_name,
                product_description=i.product_description,
                product_price=i.product_price,
                quantity=i.quantity
            )
            items.append(item)
        order = OrderDto(
                id=o.id,
                created_at=o.created_at,
                closed_at=o.closed_at,
                customer_email=o.customer_email,
                total_price=o.total_price,
                state=o.state,
                items=items
            )
        output.append(order)
    return output