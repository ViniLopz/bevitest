# Atualizado test_routes.py para cliente assíncrono
import pytest

@pytest.mark.asyncio
async def test_create_product(client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 99.99,
        "status": "em estoque",
        "stock_quantity": 10
    }
    response = await client.post("/products/", json=product_data)
    assert response.status_code == 200
    assert response.json()["name"] == product_data["name"]

@pytest.mark.asyncio
async def test_list_products(client):
    # product_data = {
    #     "name": "List Test Product",
    #     "description": "Test Description",
    #     "price": 50.00,
    #     "status": "em_estoque",
    #     "stock_quantity": 5
    # }
    
    response = await client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0

@pytest.mark.asyncio
async def test_get_product_views(client):
    product_data = {
        "name": "View Test Product",
        "description": "Description",
        "price": 30.00,
        "status": "em estoque",
        "stock_quantity": 10,
    }
    create_response = await client.post("/products/", json=product_data)
    assert create_response.status_code == 200  # Adicione esta verificação
    response_json = create_response.json()
    assert "id" in response_json
    product_id = create_response.json()["id"]

    response = await client.get(f"/products/{product_id}")
    assert response.status_code == 200

    views_response = await client.get(f"/products/{product_id}/views")
    assert views_response.status_code == 200
    assert "views" in views_response.json()

@pytest.mark.asyncio
async def test_get_product(client):
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 99.99,
        "status": "em estoque",
        "stock_quantity": 10,
    }
    create_response = await client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    response = await client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == product_data["name"]

@pytest.mark.asyncio
async def test_update_product(client):
    product_data = {
        "name": "Old Product",
        "description": "Old Description",
        "price": 50.00,
        "status": "em estoque",
        "stock_quantity": 5,
    }
    create_response = await client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    updated_data = {
        "name": "Updated Product",
        "description": "Updated Description",
        "price": 75.00,
        "status": "em falta",
        "stock_quantity": 3,
    }
    update_response = await client.put(f"/products/{product_id}", json=updated_data)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == updated_data["name"]

@pytest.mark.asyncio
async def test_delete_product(client):
    product_data = {
        "name": "Test Product to Delete",
        "description": "Test Description",
        "price": 20.00,
        "status": "em estoque",
        "stock_quantity": 2,
    }
    create_response = await client.post("/products/", json=product_data)
    product_id = create_response.json()["id"]

    delete_response = await client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Product deleted successfully"

    get_response = await client.get(f"/products/{product_id}")
    assert get_response.status_code == 404
