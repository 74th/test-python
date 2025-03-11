from fastapi import FastAPI, HTTPException, status
from uuid import UUID
from models import Todo, TodoCreate, TodoUpdate
from database import db

app = FastAPI(
    title="TODO API",
    description="A simple API for managing TODO items",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    """Initialize the database with 2 TODOs on startup"""
    db.create_todo(TodoCreate(title="First TODO", description="This is the first TODO", completed=False))
    db.create_todo(TodoCreate(title="Second TODO", description="This is the second TODO", completed=False))

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Welcome to the TODO API"}

@app.get("/todos", response_model=list[Todo])
async def get_todos():
    """Get all TODOs"""
    return db.get_todos()

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: UUID):
    """Get a single TODO by ID"""
    todo = db.get_todo(todo_id)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO with ID {todo_id} not found"
        )
    return todo

@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
async def create_todo(todo_create: TodoCreate):
    """Create a new TODO"""
    return db.create_todo(todo_create)

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: UUID, todo_update: TodoUpdate):
    """Update an existing TODO"""
    todo = db.update_todo(todo_id, todo_update)
    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO with ID {todo_id} not found"
        )
    return todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: UUID):
    """Delete a TODO"""
    success = db.delete_todo(todo_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"TODO with ID {todo_id} not found"
        )

@app.delete("/todos", status_code=status.HTTP_200_OK)
async def delete_all_todos():
    """Delete all TODOs and return the count of deleted items"""
    count = db.delete_all_todos()
    return {"deleted_count": count, "message": f"{count} TODOs have been deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)