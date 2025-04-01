import pytest
from sqlalchemy.orm import Session
from unittest.mock import MagicMock, patch

from app.model.dao import Product, Order, OrderItem, OrderState
from app.model.dto import CreateOrderItemDto, CreateOrderReqDto, OrderItemDto
from app.repository.product import get_product, get_products
from app.repository.order import (
    create_order_items,
    create_order,
    get_order,
    get_orders,
    delete_order_items,
    update_order,
    delete_order
)


# TODO: add tests for all CRUD operation / resource


def test_get_product():
    db = MagicMock(spec=Session)
    product = Product(id=1, seller_email='seller@test.com', name='Test Product', description='A test product', price=10.0, stock=5)
    db.query.return_value.filter.return_value.first.return_value = product
    
    result = get_product(db, _id=1)
    assert result.id == 1
    assert result.name == 'Test Product'

def test_get_products():
    db = MagicMock(spec=Session)
    products = [
        Product(id=1, seller_email='seller@test.com', name='Product1', description='Desc1', price=10.0, stock=5),
        Product(id=2, seller_email='seller@test.com', name='Product2', description='Desc2', price=15.0, stock=3),
    ]
    db.query.return_value.filter.return_value.all.return_value = products
    
    result = get_products(db, _ids=[1, 2])
    assert len(result) == 2
    assert result[0].id == 1
    assert result[1].id == 2

def test_create_order_items():
    db = MagicMock(spec=Session)
    product = Product(id=1, seller_email='seller@test.com', name='Test Product', description='A test product', price=10.0, stock=5)

    order = Order(id=1, customer_email='customer@test.com', total_price=0)

    order_request = CreateOrderReqDto(
        items=[CreateOrderItemDto(product_id=1, quantity=2)],
        customer_email="dummy@address.com"
    )

    with patch("app.repository.order_item.get_product", return_value=product):
        create_order_items(db, order_request, order)
    
    assert order.total_price == 20.0
    assert product.stock == 3

def test_create_order_items_insufficient_stock():
    db = MagicMock(spec=Session)
    product = Product(id=1, seller_email='seller@test.com', name='Test Product', description='A test product', price=10.0, stock=5)

    order = Order(id=1, customer_email='customer@test.com', total_price=0)

    order_request = CreateOrderReqDto(
        items=[CreateOrderItemDto(product_id=1, quantity=20)],
        customer_email="dummy@address.com"
    )

    with pytest.raises(ValueError, match='Not enough stock for product 1'):
        with patch("app.repository.order_item.get_product", return_value=product):
            create_order_items(db, order_request, order)

def test_create_order():
    db = MagicMock(spec=Session)
    order_request = CreateOrderReqDto(customer_email='customer@test.com', items=[], message='New order')
    db.begin.return_value.__enter__.return_value = db
    
    order = create_order(db, order_request)
    
    assert order.customer_email == 'customer@test.com'
    assert order.state == OrderState.CREATED

def test_delete_order():
    db = MagicMock(spec=Session)
    db.query.return_value.filter.return_value.delete.return_value = 1
    
    delete_order(db, order_id=1)
    db.query.return_value.filter.return_value.delete.call_count == 2
