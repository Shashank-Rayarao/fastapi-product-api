#pydantic is used for data validation, we dont have to write a separate init method for the class)

from pydantic import BaseModel


class Products(BaseModel):
    id :int
    name : str
    description : str
    price : int
    quantity : int
    
    # def __init__(self, id : int, name : str, description : str , price : int , quantity : int):
    #     self.id = id
    #     self.name = name
    #     self.description = description
    #     self.price = price
    #     self.quantity = quantity
        
    