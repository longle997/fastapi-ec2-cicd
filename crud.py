from sqlalchemy.orm import Session
from typing import List, Optional
import models
import schemas

def get_items(db: Session, skip: int = 0, limit: int = 100) -> List[models.Item]:
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_item(db: Session, item_id: int) -> Optional[models.Item]:
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    db_item = models.Item(
        name=item.name,
        description=item.description,
        price=item.price,
        is_available=item.is_available
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate) -> Optional[models.Item]:
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db_item.name = item.name
        db_item.description = item.description
        db_item.price = item.price
        db_item.is_available = item.is_available
        db.commit()
        db.refresh(db_item)
        return db_item
    return None

def delete_item(db: Session, item_id: int) -> Optional[models.Item]:
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return db_item
    return None
