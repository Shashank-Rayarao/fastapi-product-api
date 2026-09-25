from fastapi import FastAPI, Depends
from models import Products
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app = FastAPI()

database_models.Base.metadata.create_all(bind=engine)


@app.get("/")
def greet():
    return "Welcome to my track" 


""" use the below code if  you are not using a pydantic model in your models.py file  


products = [
    Products(1, "Phone", "budget friendly", 100, 100),
    Products(2, "Laptop", "gaming laptop", 2000, 50),
    Products(3, "buds", "Active noise cancellation", 30, 30),
]
"""  

products = [
    Products(id = 1, name = "Phone", description = "budget friendly", price = 100, quantity = 100),
    Products(id = 2, name = "Laptop", description = "gaming laptop", price = 2000, quantity = 50),
    Products(id = 3, name = "buds", description = "Active noise cancellation", price = 30, quantity = 30),
    Products(id = 6, name = "watch", description = "Smart watch", price = 300, quantity = 20),
]



def init_db():
    #database connection
    db = session()
    count = db.query(database_models.Products).count
    
    if count == 0:
        for product in products:
            db.add(database_models.Products(**products.model_dump()))
            
        db.commit()
        
init_db()            


"""
# The below code is used if the data is stored in a list inside the code itself.

@app.get("/products")
def get_all_products():
    return products
    
"""

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()
        
        
# The below code is used if the data is stored in a database and we are fetching it from there.

@app.get("/products")
def get_all_products(db: Session = Depends(get_db)):
    
    db_products = db.query(database_models.Products).all()
    return db_products
    


"""
#  The below code is used if the data is stored in a list inside the code and fetching a single product using the id

@app.get("/product/{id}")
def get_product_by_id(id : int):
    for product in products:
        if product.id == id:
            return product

    return "product not found"
"""


# The below code is used if the data is stored in a database and we are fetching a single product using the id


@app.get("/products/{id}")
def get_products_by_id(id:int, db:Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        return db_product
    return "product not found"

"""
# This code is for adding a new record through post method into the list inside the code itself.

@app.post("/product")
def add_product(product : Products):
    products.append(product)
    return product
"""

#This code is for adding a new record through post method into the database.

@app.post("/product")
def add_product(product: Products, db: Session = Depends(get_db)):
    db.add(database_models.Products(**product.model_dump()))
    db.commit()
    return product


"""
# updating an existing record from the list inside the code itself. (This is not a good practice, we should use database for storing data)

@app.put("/product")
def update_product(id : int, product : Products):
    for i in range(len(products)):
        if products[i].id == id:
            products[i] = product
            return "Product added successfully"
        
    return "product not found"   """ 

# This code is for updating an existing record from the database.

@app.put('/product')
def update_product(id:int, product: Products, db:Session = Depends(get_db)):
     db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
     if db_product:
         db_product.name = product.name
         db_product.description = product.description
         db_product.price = product.price
         db_product.quantity = product.quantity
         db.commit()
         return "product updated successfully"
     else:
         return "No product found"     


"""
# the below code is for deleting a record from the list inside the code itself.
@app.delete("/product")
def delete_product(id : int):
    for i in range(len(products)):
        if products[i].id == id:
            del products[i]
            return "Product deleted successfully"        
        
    return "Product not found"    
    
"""

# the below code is for deleting a record from the database.
@app.delete("/product")
def delete_product(id: int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Products).filter(database_models.Products.id == id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    return "Product not found"
