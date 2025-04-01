from datetime import datetime
from typing import List, Optional
from sqlalchemy import Column, Index, Integer, String, ForeignKey, Float, Enum, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import Mapped, mapped_column

from app.typing import OrderState


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    seller_email: Mapped[str] = mapped_column(String(250), index=True)
    name: Mapped[str] = mapped_column(String(500), index=True)
    description: Mapped[Optional[str]] = mapped_column(String(5000))
    manufacturer: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    stocked_at: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    price: Mapped[float]
    stock: Mapped[int]

    order_items: Mapped[Optional[List['OrderItem']]] = relationship(
        back_populates="product",
        #cascade="all, delete",
        lazy="joined"
    )


class Order(Base):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(index=True)
    closed_at: Mapped[datetime] = mapped_column(nullable=True, index=True)
    customer_email: Mapped[str] = mapped_column(String(250), index=True)
    state: Mapped[OrderState] = mapped_column(index=True)
    total_price: Mapped[float]

    items: Mapped[Optional[List['OrderItem']]] = relationship(
        back_populates="order",
        cascade="all, delete",
        lazy="joined"
    )


class OrderItem(Base):
    __tablename__ = "order_item"

    order_id: Mapped[int] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"), primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True, nullable=True, index=True)
    product_name: Mapped[str] = mapped_column(String(500))
    product_description: Mapped[str] = mapped_column(String(5000), nullable=True)
    product_price: Mapped[float]
    quantity: Mapped[int]

    order: Mapped[Optional[Order]] = relationship(
        back_populates="items", 
        lazy="joined"
    )
    product: Mapped[Optional[Product]] = relationship(
        back_populates="order_items", 
        lazy="joined",
        passive_deletes=True
    )