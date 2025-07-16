from fastapi import FastAPI, HTTPException  # Import FastAPI to create the app, and HTTPException to handle custom errors
from pydantic import BaseModel  # Import BaseModel from Pydantic to define data schemas with validation
from typing import Optional  # Import Optional for optional fields in PATCH requests
from mangum import Mangum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(root_path="/Prod")  # Create a FastAPI instance (this is your web app)

items = []  # A simple in-memory list to store items (acts like a mock database)
next_id = 1  # A counter to assign unique IDs to items

# Define a data model for incoming item data
class Item(BaseModel):  
    name: str  # Required field: item name
    price: float = 0.0  # Optional field with default value: price
    description: str = ""  # Optional field with default value: description

# Define a data model for partial updates (PATCH requests)
class ItemUpdate(BaseModel):
    name: Optional[str] = None  # Optional field: item name
    price: Optional[float] = None  # Optional field: price
    description: Optional[str] = None  # Optional field: description

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.put("/items/{item_id}")  # Register a PUT route to update an item by ID
def update_item(item_id: int, item: Item):  # The item_id from the URL path is passed in as an integer, and the request body must match the Item model
    global items  # Use the global items list
    if item_id < 1 or item_id > len(items):  # If the ID is out of range...
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
        
    
    # Update the item with new data while preserving the original ID
    item_dict = item.model_dump()  # Convert the Pydantic model to a standard Python dict
    item_dict["id"] = item_id  # Keep the original ID
    items[item_id - 1] = item_dict  # Update the item in the list (item_id is 1-based, list is 0-based)
    return item_dict  # Return the updated item

@app.delete("/items/{item_id}")  # Register a DELETE route to remove an item by ID
def delete_item(item_id: int):  # The item_id from the URL path is passed in as an integer
    global items, next_id  # Use the global items list and next_id counter
    if item_id < 1 or item_id > len(items):  # If the ID is out of range...
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")  # ...return 404 Not Found
    
    deleted_item = items.pop(item_id - 1)  # Remove and get the item (item_id is 1-based, list is 0-based)
    return {"message": f"Item {item_id} deleted successfully", "deleted_item": deleted_item}

@app.patch("/items/{item_id}")  # Register a PATCH route to partially update an item by ID
def patch_item(item_id: int, item_update: ItemUpdate):  # The item_id from the URL path is passed in as an integer, and the request body contains partial update data
    global items  # Use the global items list
    if item_id < 1 or item_id > len(items):  # If the ID is out of range...
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")  # ...return 404 Not Found
    
    # Get the existing item
    existing_item = items[item_id - 1]  # Get the current item (item_id is 1-based, list is 0-based)
    
    # Update only the fields that were provided in the request
    update_data = item_update.model_dump(exclude_unset=True)  # Get only the fields that were explicitly set
    for field, value in update_data.items():
        existing_item[field] = value  # Update the specific field
    
    return existing_item  # Return the updated item

handler = Mangum(app)
