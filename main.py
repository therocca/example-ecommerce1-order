from fastapi import FastAPI, Depends, HTTPException

from app.model.dto import CreateOrderReqDto, CreateOrderRespDto, OrderDto, ProductDto

from app.service.product import ProductService
from app.service.order import OrderService


app = FastAPI()


# TODO: add missing error handling logics, and mapping to some HTTP code and responses

# @app.post("/product/", response_model=int)                                # TODO: example of method with to-be error handling, which also defines some domain exceptions
# async def create_product(product: ProductDto,                             #       ideally make this logic a decorator for each API method
#                          product_srv: ProductService = Depends()):
#     try:
#        response = product_srv.create(product)
#        return response
#     except CustomException:
#        raise HTTPException(status_code=404, detail="Example mapped exception")


@app.post("/product/", response_model=int)
async def create_product(product: ProductDto,
                         product_srv: ProductService = Depends()):
    response = product_srv.create(product)
    return response

@app.post("/order/", response_model=CreateOrderRespDto)
async def create_order(order: CreateOrderReqDto, 
                       order_srv: OrderService = Depends()):
    response = order_srv.create(order)
    return response


@app.get("/order/{order_id}", response_model=OrderDto)
async def get_order(order_id: int,
                     order_srv: OrderService = Depends()):
    response = order_srv.get(order_id)
    return response


@app.get("/orders/", response_model=list[OrderDto])
async def get_orders(search_query: str = None, 
                     order_srv: OrderService = Depends()):
    response = order_srv.get_all(query=search_query)
    return response


@app.put("/order/{order_id}", response_model=CreateOrderRespDto)
def update_order(order_id: int, 
                 order: CreateOrderReqDto,
                 order_srv: OrderService = Depends()):
    response = order_srv.update(order_id, order)
    return response


@app.delete("/order/{order_id}")
async def delete_order(order_id: int,
                       order_srv: OrderService = Depends()) -> bool:
    response = order_srv.delete(order_id)
    return response
