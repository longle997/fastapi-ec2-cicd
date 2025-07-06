# Simple FastAPI Project

A simple FastAPI application with Docker support that provides a REST API for managing items.

## Features

- **FastAPI**: Modern, fast web framework for building APIs
- **Pydantic**: Data validation using Python type annotations
- **Docker**: Containerized application for easy deployment
- **Health Check**: Built-in health check endpoint
- **CRUD Operations**: Create, Read, Update, Delete operations for items

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /items` - Get all items
- `GET /items/{item_id}` - Get specific item by ID
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update existing item
- `DELETE /items/{item_id}` - Delete item

## Running the Application

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and run the application
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# Stop the application
docker-compose down
```

### Option 2: Using Docker directly

```bash
# Build the Docker image
docker build -t fastapi-simple .

# Run the container
docker run -p 8000:8000 fastapi-simple
```

### Option 3: Running locally (without Docker)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Accessing the Application

Once the application is running, you can access:

- **API**: http://localhost:8000
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Example Usage

### Create an item
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 999.99,
    "is_available": true
  }'
```

### Get all items
```bash
curl http://localhost:8000/items
```

### Get specific item
```bash
curl http://localhost:8000/items/1
```

### Update an item
```bash
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Laptop",
    "description": "Updated gaming laptop",
    "price": 1299.99,
    "is_available": true
  }'
```

### Delete an item
```bash
curl -X DELETE http://localhost:8000/items/1
```

## Project Structure

```
.
├── main.py              # FastAPI application
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── .gitignore          # Git ignore file
└── README.md           # This file
```

## Docker Configuration

The Dockerfile includes:
- Python 3.11 slim base image
- Non-root user for security
- Health check configuration
- Optimized layer caching
- Security best practices

## Development

To extend this project:

1. Add new endpoints in `main.py`
2. Create new Pydantic models for data validation
3. Add environment variables for configuration
4. Implement database integration (PostgreSQL, MongoDB, etc.)
5. Add authentication and authorization
6. Add logging and monitoring
7. Add unit tests

## Dependencies

- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation

## License

This project is open source and available under the [MIT License](LICENSE).
