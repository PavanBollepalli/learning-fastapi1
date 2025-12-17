from fastapi import FastAPI,Depends
from models import Product
from database import session,engine
from sqlalchemy.orm import Session
import database_models
from fastapi.middleware.cors import CORSMiddleware
app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:3900"])
database_models.base.metadata.create_all(bind=engine)

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()

# def init_db(db:Session = Depends(get_db)):
#     for product in products:
#         db.add(database_models.Product(**product.model_dump()))
#     db.commit()
# init_db()

@app.get("/")
def greet():
    return "Welcome to pavans trac"

@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):
    db_products=db.query(database_models.Product).all()
    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    return db_product

@app.post("/product")
def add_product(product:Product,db:Session=Depends(get_db)):
    db_product=db.add(database_models.Product(**product.model_dump()))
    db.commit()
    return db_product

@app.put('/product/{id}')
def update_product(id:int,product:Product,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db_product.name=product.name
        db_product.description=product.description
        db_product.price=product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product updated"
    else:
        return "Product doesnt exist"

@app.delete("/product/{id}")
def delete_product(id:int,db:Session=Depends(get_db)):
    db_product=db.query(database_models.Product).filter(database_models.Product.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
    else:
        return f'Product with ${id} doesnt exist'