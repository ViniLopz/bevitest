from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from app.models.product import Product, ProductStatus
from app.database.connection import get_db
from pydantic import BaseModel, Field
from typing import List, Optional
from pymongo import MongoClient
from datetime import datetime

# Configuração MongoDB
mongo_client = MongoClient("mongodb://mongodb:27017/")
mongo_db = mongo_client["product_logs"]
logs_collection = mongo_db["product_views"]

# Inicializando o roteador FastAPI
router = APIRouter()

# Modelos Pydantic
class ProductCreate(BaseModel):
    name: str = Field(..., example="Product Name")
    description: Optional[str] = Field(None, example="Product Description")
    price: float = Field(..., gt=0, example=9.99)
    status: ProductStatus = Field(..., example="em_estoque")
    stock_quantity: int = Field(..., ge=0, example=10)

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float

# Rotas do controlador
@router.post("/products/", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        status=product.status,
        stock_quantity=product.stock_quantity,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products/", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    # Armazenando logs no MongoDB (ID do produto e timestamp)
    for product in products:
        log_entry = {
            "product_id": product.id,
            "timestamp": datetime.utcnow(),
        }
        logs_collection.insert_one(log_entry)
    # Retornando apenas os campos necessários
    return [{ "id": product.id, "name": product.name, "description": product.description, "price": product.price} for product in products]

@router.get("/products/{id}", response_model=ProductCreate)
def get_product(id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Armazenando logs no MongoDB (ID do produto e timestamp)
    log_entry = {
        "product_id": id,
        "timestamp": datetime.utcnow(),
    }
    logs_collection.insert_one(log_entry)

    return product

@router.put("/products/{id}", response_model=ProductResponse)
def update_product(id: int, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db_product.name = product.name
    db_product.description = product.description
    db_product.price = product.price
    db_product.status = product.status
    db_product.stock_quantity = product.stock_quantity

    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{id}")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.get("/products/{id}/views")
def get_product_views(id: int):
    views = list(logs_collection.find({"product_id": id}, {"_id": 0}))

    if not views:
        raise HTTPException(status_code=404, detail="No views found for this product")

    return {
        "product_id": id,
        "view_count": len(views),
        "views": views,
    }
