"""Module for managing MongoDB Atlas connections and basic operations."""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional

from bson import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient

class TodoRepository:
    """
    A class-based repository that manages all CRUD operations for the Todo collection
    in MongoDB, providing an abstraction layer over the pymongo driver.
    """

    def __init__(self):
        """Initializes the MongoDB connection and collection pointer."""
        load_dotenv()
        try:
            self.__mongo_uri = os.getenv("MONGO_URI")
            self.__database = os.getenv("DATABASE_NAME")
            self.__collection_name = os.getenv("COLLECTION_NAME")
            self.client = MongoClient(self.__mongo_uri)
            self.db = self.client[self.__database]
            self.collection = self.db[self.__collection_name]

            self.collection.create_index([("completed", 1)])
            print(f"Successfully connected to MongoDB: {self.__database}.{self.__collection_name}")

        except Exception as e:
            print(f"ERROR: Could not connect to MongoDB at {self.__mongo_uri}. Details: {e}")
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def _document_to_dict(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """
        Converts a MongoDB document (with ObjectId) into a standard dictionary 
        with a string 'id' key, which is required for FastAPI Pydantic models.
        """
        if document:
            document['id'] = str(document.pop('_id'))
        return document

    def get_all_todos(self) -> List[Dict[str, Any]]:
        """
        Retrieves all todo items from the collection, sorted by creation date/ID descending.
        
        Returns:
            List[Dict[str, Any]]: A list of todo dictionaries.
        """
        cursor = self.collection.find().sort([('_id', -1)])
        todos = [self._document_to_dict(doc) for doc in cursor]
        return todos

    def add_todo(self, title: str) -> Optional[Dict[str, Any]]:
        """
        Inserts a new todo item into the collection.

        Args:
            title (str): The title of the new todo item.

        Returns:
            Optional[Dict[str, Any]]: The newly created todo dictionary with its ID, or None on failure.
        """
        new_todo = {
            "title": title,
            "completed": False,
            "created_at": datetime.utcnow(),
        }
        result = self.collection.insert_one(new_todo)

        if result.inserted_id:
            # Retrieve the inserted document to return the final format
            inserted_doc = self.collection.find_one({"_id": result.inserted_id})
            return self._document_to_dict(inserted_doc)
        return None

    def update_todo(
        self,
        todo_id: str,
        title: Optional[str] = None,
        completed: Optional[bool] = None
    ) -> bool:
        """
        Updates the title or completion status of an existing todo item.

        Args:
            todo_id (str): The string representation of the MongoDB ObjectId.
            title (Optional[str]): The new title.
            completed (Optional[bool]): The new completion status.

        Returns:
            bool: True if the update was successful (one document modified), False otherwise.
        """
        update_fields = {}
        if title is not None:
            update_fields["title"] = title

        if completed is not None:
            update_fields["completed"] = completed

        if not update_fields:
            return False

        try:
            object_id = ObjectId(todo_id)
        except Exception:
            return False

        result = self.collection.update_one(
            {"_id": object_id},
            {"$set": update_fields}
        )

        return result.matched_count == 1 and result.modified_count == 1

    def delete_todo(self, todo_id: str) -> bool:
        """
        Deletes a todo item by its ID.

        Args:
            todo_id (str): The string representation of the MongoDB ObjectId.

        Returns:
            bool: True if the item was deleted, False otherwise.
        """
        try:
            object_id = ObjectId(todo_id)
        except Exception:
            return False

        result = self.collection.delete_one({"_id": object_id})
        return result.deleted_count == 1

todo_repository_instance = TodoRepository()
# todo_repository_instance.add_todo("Hello World")
# todo_repository_instance.update_todo(todo_id="68f1e814711a444f0c292cac", completed=True)
