# from fastapi.testclient import TestClient
# from main import app
# import pytest

# client = TestClient(app)

# def test_create_order():
#     response = client.post("/orders/", json={"products": [{"id": 1, "quantity": 2}]})
#     assert response.status_code == 200
#     assert "id" in response.json()

# def test_list_orders():
#     response = client.get("/orders/")
#     assert response.status_code == 200

# def test_modify_order():
#     response = client.put("/orders/1", json={"products": [{"id": 1, "quantity": 3}]})
#     assert response.status_code == 200
#     assert response.json()["products"][0]["quantity"] == 3

# def test_delete_order():
#     response = client.delete("/orders/1")
#     assert response.status_code == 200
#     assert response.json()["message"] == "Order deleted successfully"

# TODO: add testing to HTPP entrypoints such as above (outdated + missing mocks of services)
