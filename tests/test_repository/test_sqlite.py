from datetime import datetime
import pytest
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker, Session

from app.model.dao import Base, Product, Order, OrderState, OrderItem
from app.model.dto import CreateOrderItemDto, CreateOrderReqDto, OrderItemDto
from app.repository.product import delete_product, get_product, get_products
from app.repository.order import create_order, delete_order, update_order


# TODO: add tests for all CRUD operation / resource


DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_session():
    """
    Fixture to provide a temp in-memory database session for testing
    """
    
    engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # Cleanup

def test_get_product(db_session: Session):
    product = Product(seller_email="seller@test.com", name="Test Product", description="A test product", price=10.0, stock=5)
    db_session.add(product)
    db_session.commit()

    product = get_product(db_session, _id=1)
    assert product is not None
    assert product.name == "Test Product"
    assert product.price == 10.0

def test_create_order(db_session: Session):
    product1 = Product(
        id=1, 
        seller_email="seller1@test.com", 
        name="Test Product1", 
        description="A test product", 
        price=10.0, 
        stock=5
    )
    db_session.add(product1)
    product2 = Product(
        id=2, 
        seller_email="seller2@test.com", 
        name="Test Product2", 
        description="A test product", 
        price=1.5, 
        stock=20
    )
    db_session.add(product2)
    db_session.commit()

    request_msg = "I really want these things!"
    order_request = CreateOrderReqDto(items=[
            CreateOrderItemDto(product_id=1, quantity=2),
            CreateOrderItemDto(product_id=2, quantity=5)
        ],
        customer_email="customer@test.com",
        message=request_msg
    )

    create_order(db_session, order_request)

    product = db_session.query(Product).filter_by(id=1).first()
    assert product.stock == 3

    product = db_session.query(Product).filter_by(id=2).first()
    assert product.stock == 15

    order = db_session.query(Order).first()
    assert order.state == OrderState.CREATED
    assert order.total_price == 27.5

    order_item = db_session.query(OrderItem).filter(OrderItem.order_id==order.id,OrderItem.quantity==2).first()
    assert order_item.product_id == 1
    assert order_item.product_name == 'Test Product1'
    assert order_item.product_description == 'A test product'
    assert order_item.product_price == 10.0

def test_update_order(db_session: Session):
    product1 = Product(
        id=1, 
        seller_email="seller1@test.com", 
        name="Test Product1", 
        description="A test product", 
        price=10.0, 
        stock=5
    )
    db_session.add(product1)
    product2 = Product(
        id=2, 
        seller_email="seller2@test.com", 
        name="Test Product2", 
        description="A test product", 
        price=1.5, 
        stock=20
    )
    db_session.add(product2)
    created_at = datetime.now()
    order = Order(
        id=1,
        created_at = created_at,
        customer_email="customer1@test.com",
        total_price=27.5,
        state=OrderState.CREATED,
        items=[
            OrderItem(product_id=1, quantity=2, product_name="Test Product1", product_price=10.),
            OrderItem(product_id=2, quantity=5, product_name="Test Product2", product_price=1.5)
        ]
    )
    db_session.add(order)
    db_session.commit()

    request_msg = "I want to change the quantities I have previously purchased"
    order_request = CreateOrderReqDto(items=[
            CreateOrderItemDto(product_id=1, quantity=1),
            CreateOrderItemDto(product_id=2, quantity=6)
        ],
        customer_email="customer@test.com",
        message=request_msg
    )

    update_order(db_session, 1, order_request)

    product = db_session.query(Product).filter_by(id=1).first()
    assert product.stock == 6

    product = db_session.query(Product).filter_by(id=2).first()
    assert product.stock == 19

    order = db_session.query(Order).first()
    assert order.state == OrderState.CHANGED
    assert order.total_price == 19.0

def test_delete_order(db_session: Session):
    # Add products
    product1 = Product(
        id=1, 
        seller_email="seller1@test.com", 
        name="Test Product1", 
        description="A test product", 
        price=10.0, 
        stock=5
    )
    db_session.add(product1)
    product2 = Product(
        id=2, 
        seller_email="seller2@test.com", 
        name="Test Product2", 
        description="A test product", 
        price=1.5, 
        stock=20
    )
    db_session.add(product2)

    # Add orders
    created_at = datetime.now()
    order = Order(
        id=1,
        created_at = created_at,
        customer_email="customer1@test.com",
        total_price=27.5,
        state=OrderState.CREATED,
        items=[
            OrderItem(product_id=1, quantity=2, product_name="Test Product1", product_price=10.),
            OrderItem(product_id=2, quantity=5, product_name="Test Product2", product_price=1.5)
        ]
    )
    db_session.add(order)
    db_session.commit()

    order = Order(
        id=2,
        created_at = created_at,
        customer_email="customer1@test.com",
        total_price=27.5,
        state=OrderState.CREATED,
        items=[
            OrderItem(product_id=1, quantity=2, product_name="Test Product1", product_price=10.),
        ]
    )
    db_session.add(order)
    db_session.commit()

    # Test
    delete_order(db_session, 1)

    orders = db_session.query(Order).all()
    assert len(orders) == 1
    order = orders[0]
    assert order.id == 2
    orders_items = db_session.query(OrderItem).all()
    assert len(orders_items) == 1
    orders_item = orders_items[0]
    assert orders_item.order_id == 2

def test_delete_product_keep_old_items_info(db_session: Session):
    # Add products
    product1 = Product(
        id=1, 
        seller_email="seller1@test.com", 
        name="Test Product1", 
        description="A test product", 
        price=10.0, 
        stock=5
    )
    db_session.add(product1)
    product2 = Product(
        id=2, 
        seller_email="seller2@test.com", 
        name="Test Product2", 
        description="A test product", 
        price=1.5, 
        stock=20
    )
    db_session.add(product2)

    # Add orders
    created_at = datetime.now()
    order = Order(
        id=1,
        created_at = created_at,
        customer_email="customer1@test.com",
        total_price=27.5,
        state=OrderState.CREATED,
        items=[
            OrderItem(product_id=1, quantity=2, product_name="Test Product1", product_price=10.),
            OrderItem(product_id=2, quantity=5, product_name="Test Product2", product_price=1.5)
        ]
    )
    db_session.add(order)
    db_session.commit()

    # Test
    delete_product(db_session, 1)

    product = db_session.query(Product).filter(Product.id==1).first()
    assert product is None
    order_item = db_session.query(OrderItem).filter(OrderItem.order_id==1,OrderItem.quantity==2).first()
    assert order_item.product_id is None
    assert order_item.product_name == 'Test Product1'
    assert order_item.product_price == 10.0
    order_item = db_session.query(OrderItem).filter(OrderItem.order_id==1,OrderItem.quantity==5).first()
    assert order_item.product_id is not None