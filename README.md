# Example-ecommerce1-order
Example of a microservice which handles some products and orders inside an ecommerce application

# Conda build
```bash
conda create --name example-ecommerce1 python=3.12
conda activate example-ecommerce1
pip install -r requirements.txt
```

# Run data layer
```bash
docker-compose up -d
```

# Run app layer
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

you can interact with the Swagger UI at localhost:8000/docs

# Note to reviewers
Main assumptions / requirements (also for time constraints):

- assume no other product catalogue microservices to sync with
- assume the source of truth of the service is the relational DB
- additional requirement added (just to show a possibility which can be useful in a given scenario):
    - when an order is created, it maintains a link between OrderItem and Product, but also copy some fields of the product in the item
    - this can be useful in case we want to store the information of the order at the date when was created, independently from product state
    - in this way we can, for example, delete a product while maintaining some useful values of the product inside the item (when was created)
- the as-is has capabilities for advanced search using Meili:
    - current as-is is capable of searching on the whole Order+OrderItem denormalized structure (e.g. you can search on order.created_at, order.items.product_name...); we can switch to a model for searching (for example) only inside name and description of the items

Future plans (details inside comments in the code):

- extend testing coverage
- clean and extend docs in method (e.g. args)
- extend capabilities / architecture of the as-is:
    - Redis can be used as a key-value store to increase performance on reads of order by IDs (in-memory + distributed, very fast)
    - increase response time of client request by asynchronous ingestion of orders inside Meili:
        - instead of inserting synchrounously documents in the storage, we can use a combination of Redis+Celery to pubblish asynchrounously the documents, then return to the client (in this way search becomes more eventual consistent, consider also using Rabbit instead of Redis for more guarantees); we can use a cronjob in Celery which periodically ingest documents; in both cases also consider for adopting logics similar to outbox pattern, for example by adding a 'dirty_index' bool field to Order

