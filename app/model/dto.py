from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

from app.model.dao import OrderState


class ProductDto(BaseModel):
    id: Optional[int] = None
    seller_email: str
    name: str
    description: Optional[str] = None
    manufacturer: Optional[str] = None
    stocked_at: Optional[str] = None
    price: float
    stock: int


class OrderDto(BaseModel):
    id: Optional[int] = None
    created_at: datetime
    closed_at: Optional[datetime] = None
    customer_email: str
    total_price: float
    state: OrderState

    items: Optional[list['OrderItemDto']]


class OrderDto2(BaseModel):
    id: Optional[int] = None
    created_at: str
    customer_email: str
    total_price: float
    state: str

    items: Optional[list['OrderItemDto2']]


class OrderItemDto(BaseModel):
    order_id: Optional[int] = None
    product_id: Optional[int]  = None
    product_name: str
    product_description: Optional[str] = None
    product_price: float
    quantity: int


class OrderItemDto2(BaseModel):
    product_id: Optional[int]  = None
    product_name: str
    product_description: Optional[str] = None
    product_price: float
    quantity: int


class CreateOrderReqDto(BaseModel):
    customer_email: str
    items: List['CreateOrderItemDto']


class CreateOrderItemDto(BaseModel):
    product_id: Optional[int]  = None
    quantity: int


class CreateOrderRespDto(BaseModel):
    order_id: int
    total_price: float