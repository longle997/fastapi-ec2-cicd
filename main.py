from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import uvicorn

# Import our modules
from database import engine, get_db
import models
import schemas
import crud

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Simple FastAPI Project with PostgreSQL",
    description="A simple FastAPI application with Docker support and PostgreSQL database",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Simple FastAPI Project with PostgreSQL!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "fastapi-postgresql"}

@app.get("/items", response_model=List[schemas.ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.get_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.post("/items", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db=db, item=item)

@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
def update_item(item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    db_item = crud.update_item(db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_item(db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": f"Item {item_id} deleted successfully"}

# Initialize with sample data
@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    # Check if we already have data
    if crud.get_items(db, limit=1):
        return
    
    # Create sample data
    sample_items = [
        schemas.ItemCreate(
            name="Laptop",
            description="High-performance laptop for development",
            price=999.99,
            is_available=True
        ),
        schemas.ItemCreate(
            name="Wireless Mouse",
            description="Ergonomic wireless mouse with USB receiver",
            price=29.99,
            is_available=True
        ),
        schemas.ItemCreate(
            name="Mechanical Keyboard",
            description="RGB mechanical keyboard with blue switches",
            price=149.99,
            is_available=False
        ),
        schemas.ItemCreate(
            name="Monitor",
            description="27-inch 4K monitor with USB-C connectivity",
            price=399.99,
            is_available=True
        ),
        schemas.ItemCreate(
            name="Webcam",
            description="1080p webcam with auto-focus",
            price=79.99,
            is_available=True
        )
    ]
    
    for item in sample_items:
        crud.create_item(db=db, item=item)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
