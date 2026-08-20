# Inventory Management API

A RESTful API built with FastAPI for managing product inventory. The project follows a layered architecture (Router -> Service -> Repository -> Model) with SQLAlchemy as the ORM and SQLite as the database engine. Pydantic is used for request/response validation through dedicated schemas.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Requirements](#requirements)
4. [Setup and Installation](#setup-and-installation)
5. [Running the Application](#running-the-application)
6. [API Endpoints](#api-endpoints)
7. [Data Model](#data-model)
8. [Schemas (Validation Layer)](#schemas-validation-layer)
9. [Running the Tests](#running-the-tests)
10. [Notes and Design Decisions](#notes-and-design-decisions)

## Architecture Overview

The application is organized into four main layers:

- **Router (`app/routers`)**: Defines the HTTP endpoints, receives requests, and delegates the logic to the service layer. It is also responsible for dependency injection (creating the database session, repository, and service for each request).
- **Service (`app/services`)**: Contains the business logic. It orchestrates calls to the repository and handles domain-specific rules, such as raising an HTTP 404 error when a product is not found.
- **Repository (`app/repositories`)**: Handles direct interaction with the database through SQLAlchemy (create, read, update, delete operations).
- **Model (`app/models`)**: Defines the SQLAlchemy ORM model that maps to the `products` table in the database.
- **Schema (`app/schemas`)**: Defines the Pydantic models used to validate incoming data and serialize outgoing responses.

Request flow example (creating a product):

```
Client -> Router -> Service -> Repository -> Database
                                   |
Client <- Router <- Service <- Repository (returns created object)
```

## Project Structure

```
app/
  models/
    __init__.py
    product.py          # SQLAlchemy ORM model (ProductTable)
  repositories/
    __init__.py
    product.py           # Database access logic (ProductRepository)
  routers/
    __init__.py
    product.py           # API endpoints (FastAPI router)
  schemas/
    __init__.py
    product.py           # Pydantic schemas (Create, Update, Response)
  services/
    __init__.py
    product.py            # Business logic (ProductService)
  __init__.py
  database.py             # Database engine, session, and Base declaration
  main.py                 # FastAPI application entry point
tests/
  __init__.py
  conftest.py              # Pytest fixtures (in-memory test database, test client)
  test_product_api.py      # Integration tests for the Product API
.gitignore
README.md
requirements.txt
```

## Requirements

- Python 3.10 or higher (recommended)
- pip (Python package manager)

The project dependencies, listed in `requirements.txt`, are:

- `fastapi` - Web framework used to build the API
- `uvicorn[standard]` - ASGI server used to run the FastAPI application
- `sqlalchemy` - ORM used to interact with the SQLite database
- `pydantic` - Data validation and serialization library
- `pytest` - Testing framework
- `httpx` - HTTP client required by FastAPI's `TestClient`

## Setup and Installation

Follow these steps in order to get the project running locally.

### 1. Clone or download the repository

```bash
git clone https://github.com/YamitGC/Inventory-FastAPI.git
cd Inventory-FastAPI
```

### 2. Create a virtual environment

It is strongly recommended to isolate the project dependencies inside a virtual environment.

On Linux / macOS:

```bash
python3 -m venv .venv
```

On Windows:

```bash
python -m venv .venv
```

This creates a `.venv` folder in the project root, which is already excluded from version control in `.gitignore`.

### 3. Activate the virtual environment

On Linux / macOS:

```bash
source .venv/bin/activate
```

On Windows (Command Prompt):

```bash
.venv\Scripts\activate.bat
```

On Windows (PowerShell):

```bash
.venv\Scripts\Activate.ps1
```

Once activated, your terminal prompt should be prefixed with `(.venv)`, indicating that the virtual environment is active.

### 4. Install the dependencies

With the virtual environment active, install all required packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Verify the installation (optional)

You can confirm that FastAPI and Uvicorn were installed correctly by running:

```bash
pip show fastapi uvicorn
```

## Running the Application

With the virtual environment active and dependencies installed, start the development server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

Explanation of the command:

- `app.main:app` points to the `app` FastAPI instance defined in `app/main.py`.
- `--reload` enables auto-reload on code changes, useful during development.

By default, the server will be available at:

```
http://127.0.0.1:8000
```

On startup, the application automatically creates the `products` table in the SQLite database (`inventory.db`) if it does not already exist, since `Base.metadata.create_all(bind=engine)` is called in `app/main.py`.

### Interactive API Documentation

FastAPI automatically generates interactive documentation. Once the server is running, you can access:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Root Endpoint

A simple health-check endpoint is available at the root path:

```
GET /
```

Response:

```json
{ "message": "Inventory API is running" }
```

## API Endpoints

All product-related endpoints are prefixed with `/products` and tagged as `Products`.

| Method | Endpoint           | Description                      | Success Status |
| ------ | ------------------ | -------------------------------- | -------------- |
| POST   | `/products/`     | Create a new product             | 201 Created    |
| GET    | `/products/`     | Retrieve all products            | 200 OK         |
| GET    | `/products/{id}` | Retrieve a single product by ID  | 200 OK         |
| PUT    | `/products/{id}` | Update an existing product by ID | 200 OK         |
| DELETE | `/products/{id}` | Delete a product by ID           | 204 No Content |

If a product ID does not exist, `GET`, `PUT`, and `DELETE` operations return a `404 Not Found` response with the detail message `"Product not found"`.

### Example: Create a Product

Request:

```bash
curl -X POST "http://127.0.0.1:8000/products/" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Mechanical Keyboard",
        "category": "RGB Wireless Keyboard",
        "price": 89.99,
        "stock": 15
      }'
```

Response (`201 Created`):

```json
{
  "id": 1,
  "name": "Mechanical Keyboard",
  "category": "RGB Wireless Keyboard",
  "price": 89.99,
  "stock": 15
}
```

### Example: Update a Product

Request:

```bash
curl -X PUT "http://127.0.0.1:8000/products/1" \
  -H "Content-Type: application/json" \
  -d '{
        "name": "Mechanical Keyboard Pro",
        "price": 99.99
      }'
```

Only the fields provided in the request body are updated, since the update logic uses `model_dump(exclude_unset=True)`.

### Example: Delete a Product

Request:

```bash
curl -X DELETE "http://127.0.0.1:8000/products/1"
```

Response: `204 No Content`

## Data Model

The `ProductTable` model, defined in `app/models/product.py`, maps to the `products` table with the following columns:

| Column       | Type        | Constraints          |
| ------------ | ----------- | -------------------- |
| `id`       | Integer     | Primary key, indexed |
| `name`     | String(100) | Not null             |
| `category` | String      | Not null, indexed    |
| `price`    | Float       | Not null             |
| `stock`    | Integer     | Default: 0           |

## Schemas (Validation Layer)

Defined in `app/schemas/product.py`:

- **`ProductBase`**: Shared base fields with validation rules.
  - `name`: string, length between 2 and 100 characters
  - `category`: string, length between 2 and 50 characters
  - `price`: float, must be greater than 0
  - `stock`: integer, must be greater than or equal to 0 (default 0)
- **`ProductCreate`**: Used for the `POST` endpoint. Inherits all fields from `ProductBase`.
- **`ProductUpdate`**: Used for the `PUT` endpoint. All fields are optional, allowing partial updates.
- **`ProductResponse`**: Used to serialize the data returned to the client. Includes the `id` field and is configured with `from_attributes` (formerly `orm_mode`) to allow direct conversion from SQLAlchemy model instances.

## Running the Tests

The test suite uses `pytest` along with FastAPI's `TestClient` and an isolated in-memory SQLite database, so tests do not affect the real `inventory.db` file.

With the virtual environment active and dependencies installed, run:

```bash
pytest
```

To run the tests with more detailed output:

```bash
pytest -v
```

To run a specific test file:

```bash
pytest tests/test_product_api.py
```

### How the test setup works

- `tests/conftest.py` defines two fixtures:
  - `db_session`: creates a fresh in-memory SQLite database (using `StaticPool` to keep the connection alive across threads) before each test, and drops all tables after the test finishes.
  - `client`: overrides the `get_db` dependency of the FastAPI app so that all requests during testing use the isolated `db_session` instead of the real database, then yields a `TestClient` instance.
- `tests/test_product_api.py` contains integration tests covering:
  - Creating a product
  - Listing products when the database is empty
  - Retrieving a product by ID
  - Handling a request for a non-existent product (404)
  - Updating a product
  - Deleting a product and verifying it is no longer retrievable

## Notes and Design Decisions

- The database file `inventory.db` is created automatically in the project root the first time the application starts. It is excluded from version control via `.gitignore`.
- The `check_same_thread: False` connection argument is required because SQLite, by default, only allows the thread that created a connection to use it. This is necessary for both the application server and the test suite, since FastAPI can process requests on different threads.
- The `PUT` endpoint behaves as a partial update: only fields explicitly provided in the request body are updated, since `ProductUpdate` treats all fields as optional and the repository excludes unset fields when applying changes.
- Dependency injection is used throughout the router layer (`get_db`, and the composed `get_product_service`), which also makes it possible to override the database session in tests without modifying the application code.
