from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
import uvicorn

app = FastAPI(
    title="Simple FastAPI Project",
    description="A simple FastAPI application with Docker support",
    version="1.0.0"
)

# Pydantic models
class Item(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class ItemResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool

# In-memory storage (for demo purposes)
tems_db = [
    {
        "id": 1,
        "name": "Laptop",
        "description": "High-performance laptop for development",
        "price": 999.99,
        "is_available": True
    },
    {
        "id": 2,
        "name": "Wireless Mouse",
        "description": "Ergonomic wireless mouse with USB receiver",
        "price": 29.99,
        "is_available": True
    },
    {
        "id": 3,
        "name": "Mechanical Keyboard",
        "description": "RGB mechanical keyboard with blue switches",
        "price": 149.99,
        "is_available": False
    },
    {
        "id": 4,
        "name": "Monitor",
        "description": "27-inch 4K monitor with USB-C connectivity",
        "price": 399.99,
        "is_available": True
    },
    {
        "id": 5,
        "name": "Webcam",
        "description": "1080p webcam with auto-focus",
        "price": 79.99,
        "is_available": True
    }
]
item_counter = 6

@app.get("/")
async def root():
    return {"message": "Welcome to Simple FastAPI Project!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fastapi-simple"}

@app.get("/items", response_model=List[ItemResponse])
async def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: int):
    for item in items_db:
        if item["id"] == item_id:
            return item
    return {"error": "Item not found"}

@app.post("/items", response_model=ItemResponse)
async def create_item(item: Item):
    global item_counter
    new_item = {
        "id": item_counter,
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "is_available": item.is_available
    }
    items_db.append(new_item)
    item_counter += 1
    return new_item

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: int, item: Item):
    for i, existing_item in enumerate(items_db):
        if existing_item["id"] == item_id:
            updated_item = {
                "id": item_id,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "is_available": item.is_available
            }
            items_db[i] = updated_item
            return updated_item
    return {"error": "Item not found"}

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item["id"] == item_id:
            deleted_item = items_db.pop(i)
            return {"message": f"Item {item_id} deleted successfully", "deleted_item": deleted_item}
    return {"error": "Item not found"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
