"""
Todo App Pydantic Model Definition
Defines the structure for Todo data used by the API for validation and responses.
"""

from typing import Optional
from pydantic import BaseModel, Field

class TodoBase(BaseModel):
    """Base model for Todo item data."""
    title: str = Field(..., min_length=1, max_length=100, description="The content of the todo item.")
    completed: bool = Field(False, description="Completion status of the todo item.")

class TodoCreate(BaseModel):
    """Model used for creating a new Todo (only requires title)."""
    title: str = Field(..., min_length=1, max_length=100)

class TodoUpdate(BaseModel):
    """Model used for updating a Todo (fields are optional)."""
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    completed: Optional[bool] = None

class Todo(TodoBase):
    """Full Todo model, including the ID (now a string for MongoDB ObjectId)."""
    id: str = Field(..., description="The unique MongoDB ObjectId for the todo item.")

    class Config:
        """
        Allows Pydantic to read data from MongoDB documents (e.g., when converting a Mongo dict 
        to a Pydantic model) and provides a JSON schema example.
        """
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "60a7e1c0c1b9a4a7d4e5f6d7",
                "title": "Set up MongoDB connection",
                "completed": True
            }
        }
