""" Service layer for Todo operations, mediating between API and database. """

from typing import List, Dict, Any, Optional
from db.mongo_db import todo_repository_instance as todo_repository

class TodoService:
    """
    Handles the business logic for Todo items, mediating between the 
    API (routers) and the database (repository).
    """

    def __init__(self, repository=todo_repository):
        """Initializes the service with the repository instance."""
        self.repository = repository

    def list_todos(self) -> List[Dict[str, Any]]:
        """Retrieves all todos from the database."""
        return self.repository.get_all_todos()

    def create_todo(self, title: str) -> Optional[Dict[str, Any]]:
        """Creates a new todo item."""
        return self.repository.add_todo(title)

    def update_todo(
        self,
        todo_id: str,
        title: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> bool:
        """Updates an existing todo."""
        return self.repository.update_todo(todo_id, title, completed)

    def delete_todo(self, todo_id: str) -> bool:
        """Deletes a todo."""
        return self.repository.delete_todo(todo_id)

# def get_todo_service() -> TodoService:
#     """Returns an instance of the TodoService."""
#     return TodoService()
