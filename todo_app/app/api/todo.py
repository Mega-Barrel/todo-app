"""
Todo FastAPI Routers
"""
from typing import List

from fastapi import APIRouter, HTTPException, Body, Depends, Path
from models.todo import Todo, TodoCreate, TodoUpdate
from services.todo import TodoService

def get_todo_service() -> TodoService:
    """Returns an instance of the TodoService."""
    return TodoService()

router = APIRouter(tags=["Todos"])

@router.get("/todos", response_model=List[Todo])
def list_todos(service: TodoService = Depends(get_todo_service)):
    """Retrieve all todo items."""
    return service.list_todos()

@router.post("/todos", response_model=Todo, status_code=201)
def create_todo(
    todo_item: TodoCreate,
    service: TodoService = Depends(get_todo_service)
):
    """Create a new todo item."""
    new_todo = service.create_todo(todo_item.title)
    if new_todo:
        return new_todo
    raise HTTPException(status_code=500, detail="Could not create todo item.")

@router.put("/todos/{todo_id}", response_model=dict)
def update_existing_todo(
    todo_id: str = Path(..., min_length=24, max_length=24, description="MongoDB ObjectId"),
    todo_update: TodoUpdate = Body(...),
    service: TodoService = Depends(get_todo_service)
):
    """Update an existing todo item's title or completion status."""
    title = todo_update.title
    completed = todo_update.completed

    if not service.update_todo(todo_id, title, completed):
        raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found or invalid ID provided.")
    return {"message": f"Todo {todo_id} updated successfully."}

@router.delete("/todos/{todo_id}", status_code=204)
def delete_existing_todo(
    todo_id: str = Path(..., min_length=24, max_length=24, description="MongoDB ObjectId"),
    service: TodoService = Depends(get_todo_service)
):
    """Delete a todo item by ID."""
    if not service.delete_todo(todo_id):
        raise HTTPException(status_code=404, detail=f"Todo with ID {todo_id} not found or invalid ID provided.")
    return
