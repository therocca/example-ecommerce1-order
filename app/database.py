from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.model.dao import Base


MARIADB_DATABASE_URL = "mariadb+pymysql://root:rootpassword@localhost:3306/order_service?charset=utf8mb4"

engine = create_engine(MARIADB_DATABASE_URL, pool_size=5, max_overflow=10)
SessionOrderService = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(engine)

def get_db():
    """
    Factory method for singleton DB session
    """
    db = SessionOrderService()
    try:
        yield db
    finally:
        db.close()