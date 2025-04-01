from meilisearch import Client

from app.model.dao import Order
from app.model.dto import OrderDto
from app.model.mapper import order_to_dto2, orders_dto_from_dict


client = Client('http://localhost:7700')
index = client.index('order')


def create_index(index_name: str):
    index.delete()                              # TODO: clean entire file, here just used for dev (delete if existing)
    client.create_index(index_name)


def search_orders(query) -> list[OrderDto]:
    orders = index.search(query)['hits']
    orders = orders_dto_from_dict(orders)
    return orders


def index_order(order: Order):
    order_dto = order_to_dto2(order)
    orders = [order_dto.model_dump()]
    index.add_documents(orders)
    # print("Added")


def remove_index_order(order_id: int):
    # print(_id)
    index.delete_document(order_id)