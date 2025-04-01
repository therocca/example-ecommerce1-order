from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.model.dto import CreateOrderReqDto, CreateOrderRespDto, OrderDto
from app.model.mapper import order_to_dto, orders_to_dto
import app.repository.order as order_repo
from app.search import index_order, remove_index_order, search_orders
# from app.cache import redis_client


class OrderService:
    """
    Class for CRUD service on Order resource.
    """

    def __init__(self, db: Session = Depends(get_db),):
        self.db = db

    def create(self, order: CreateOrderReqDto) -> CreateOrderRespDto:
        new_order = order_repo.create_order(self.db, order)
        # key = f"order:{order_id}"                                                 # TODO: add support for redis caching on get by ID, faster, more scalable, in-memory
        # redis_client.setex(key, expire, json.dumps(order_data))
        index_order(new_order)                                                      # TODO: instead of sync ingestion in Meili, we can just forward async with Redis for later ingestion, which makes overall client request faster
        response = CreateOrderRespDto(                                              # TODO: move to DTO mapper method
            order_id=new_order.id,
            total_price=new_order.total_price
        )
        return response
    
    def get(self, order_id: int) -> OrderDto:
        order = order_repo.get_order(self.db, _id=order_id)
        response = order_to_dto(order)
        # key = f"order:{order_id}"                                                 # TODO: redis read
        # order_json = redis_client.get(key)  # Fetch order from Redis
        return response

    def get_all(self, query: str = None) -> list[OrderDto]:                         # TODO: add possibility also for read filtered from DB (e.g. + query params to filter on field state in DB query)
        if query:
            return search_orders(query)
        orders = order_repo.get_orders(self.db)
        response = orders_to_dto(orders)
        return response

    def update(self, order_id: int, order: CreateOrderReqDto) -> CreateOrderRespDto:
        existing_order = order_repo.update_order(self.db, order_id, order)
        # key = f"order:{order_id}"                                                 # TODO: redis delete, re updated on next get
        # redis_client.delete(key)
        index_order(existing_order)
        response = CreateOrderRespDto(                                              # TODO: move to DTO mapper method
            order_id=existing_order.id,
            total_price=existing_order.total_price
        )
        return response

    def delete(self, order_id: int) -> bool:
        order_repo.delete_order(self.db, order_id)
        # key = f"order:{order_id}"                                                 # TODO: redis delete, re updated on next get
        # redis_client.delete(key)
        remove_index_order(order_id)
        return True
