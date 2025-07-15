from fastapi import FastAPI, HTTPException  # Import FastAPI to create the app, and HTTPException to handle custom errors
from pydantic import BaseModel  # Import BaseModel from Pydantic to define data schemas with validation

app = FastAPI()  # Create a FastAPI instance (this is your web app)

items = []  # A simple in-memory list to store items (acts like a mock database)
next_id = 1  # A counter to assign unique IDs to items

# Define a data model for incoming item data
class Item(BaseModel):  
    name: str  # Required field: item name
    price: float = 0.0  # Optional field with default value: price
    description: str = ""  # Optional field with default value: description

@app.get("/")  # Register a GET route at the root (http://localhost:8000/)
def read_root():  
    return {"Hello from": "FastAPI"}  # Return a simple JSON response

@app.get("/items/")  # Register a GET route at /items/ to list all items
def get_items():
    return {"items": items}  # Return the current list of items

@app.post("/items/")  # Register a POST route at /items/ to create a new item
def create_item(item: Item):  # Accepts a request body matching the Item model
    global next_id  # Use the global counter to assign unique IDs
    item_dict = item.model_dump()  # Convert the Pydantic model to a standard Python dict
    item_dict["id"] = next_id  # Add an ID to the item
    next_id += 1  # Increment the ID counter for the next item
    items.append(item_dict)  # Add the new item to the items list
    return item_dict  # Return the created item as the response

@app.get("/items/{item_id}")  # Register a dynamic GET route to retrieve one item by ID
def get_item(item_id: int):  # The item_id from the URL path is passed in as an integer
    if item_id < 1 or item_id > len(items):  # If the ID is out of range...
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")  # ...return 404 Not Found

    item = items[item_id - 1]  # List index starts from 0, but item IDs start from 1
    return item  # Return the requested item
