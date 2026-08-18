from fastapi import status


def test_create_product(client):
    # Arrange: Define payload for new product
    payload = {
        "name": "Mechanical Keyboard",
        "category": "RGB Wireless Keyboard",
        "price": 89.99,
        "stock": 15
    }

    # Act: Send POST request to create product
    response = client.post("/products/", json=payload)
    data = response.json()

    # Assert: Validate HTTP response status code and payload matching
    assert response.status_code == status.HTTP_201_CREATED
    assert data["name"] == payload["name"]
    assert data["price"] == payload["price"]
    assert data["stock"] == payload["stock"]
    assert "id" in data


def test_get_all_products_empty(client):
    # Act: Send GET request when database has no records
    response = client.get("/products/")

    # Assert: Should return HTTP 200 and an empty list
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []


def test_get_product_by_id(client):
    # Arrange: Create a product first
    payload = {
        "name": "Gaming Mouse",
        "category": "Ergonomic Optical Mouse",
        "price": 45.50,
        "stock": 30
    }
    create_res = client.post("/products/", json=payload)
    product_id = create_res.json()["id"]

    # Act: Fetch the created product by ID
    response = client.get(f"/products/{product_id}")
    data = response.json()

    # Assert: Check retrieve status and payload integrity
    assert response.status_code == status.HTTP_200_OK
    assert data["id"] == product_id
    assert data["name"] == payload["name"]


def test_get_product_not_found(client):
    # Act: Attempt to fetch non-existent product ID
    response = client.get("/products/9999")

    # Assert: Should return HTTP 404 Not Found error
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Product not found"


def test_update_product(client):
    # Arrange: Create product to update
    payload = {
        "name": "Monitor",
        "category": "24 inch Full HD",
        "price": 150.00,
        "stock": 10
    }
    create_res = client.post("/products/", json=payload)
    product_id = create_res.json()["id"]

    update_payload = {
        "name": "Monitor 4K",
        "category": "27 inch Ultra HD",
        "price": 350.00,
        "stock": 5
    }

    # Act: Send PUT request with updated data
    response = client.put(f"/products/{product_id}", json=update_payload)
    data = response.json()

    # Assert: Check updated fields
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == update_payload["name"]
    assert data["price"] == update_payload["price"]


def test_delete_product(client):
    # Arrange: Create product to delete
    payload = {
        "name": "USB Cable",
        "category": "Type-C 2m",
        "price": 9.99,
        "stock": 100
    }
    create_res = client.post("/products/", json=payload)
    product_id = create_res.json()["id"]

    # Act: Send DELETE request
    delete_res = client.delete(f"/products/{product_id}")

    # Assert: Should return HTTP 204 No Content
    assert delete_res.status_code == status.HTTP_204_NO_CONTENT

    # Verify item is no longer retrievable
    get_res = client.get(f"/products/{product_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND