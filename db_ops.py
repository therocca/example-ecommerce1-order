from app.model.dao import Base
from app.database import engine
from app.search import create_index


def create_db_datamodel():
    Base.metadata.create_all(engine)
    print("Datamodel created successfully in relational database.")


def create_ms_index():
    create_index('order')
    print("Index created successfully in search storage.")


if __name__ == "__main__":
    create_db_datamodel()
    create_ms_index()