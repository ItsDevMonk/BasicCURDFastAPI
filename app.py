from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# Pydantic models


class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# In-memory storage with default values
items = [
    Item(id=1, name="Item 1", description="Description for item 1"),
    Item(id=2, name="Item 2", description="Description for item 2")
]

# Endpoint 1: Items


@app.get("/items", response_model=List[Item])
def read_items(request: Request):
    # print the headers
    print(request.headers)
    return items


@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    new_item = Item(id=len(items) + 1, **item.dict())
    items.append(new_item)
    return new_item


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemUpdate):
    for i in range(len(items)):
        if items[i].id == item_id:
            items[i] = items[i].copy(update=item.dict(exclude_unset=True))
            return items[i]
    raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    for i in range(len(items)):
        if items[i].id == item_id:
            return items.pop(i)
    raise HTTPException(status_code=404, detail="Item not found")

# Endpoint 2: Users


class User(BaseModel):
    id: int
    username: str
    email: str


class UserCreate(BaseModel):
    username: str
    email: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None


# In-memory storage with default values
users = [
    User(id=1, username="user1", email="user1@example.com"),
    User(id=2, username="user2", email="user2@example.com")
]


@app.get("/users", response_model=List[User])
def read_users(request: Request):
    print(request.headers)
    return users


@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    new_user = User(id=len(users) + 1, **user.dict())
    users.append(new_user)
    return new_user


@app.put("/users/{user_id}", response_model=User)
def update_user(user_id: int, user: UserUpdate):
    for i in range(len(users)):
        if users[i].id == user_id:
            users[i] = users[i].copy(update=user.dict(exclude_unset=True))
            return users[i]
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/users/{user_id}", response_model=User)
def delete_user(user_id: int):
    for i in range(len(users)):
        if users[i].id == user_id:
            return users.pop(i)
    raise HTTPException(status_code=404, detail="User not found")


# run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
