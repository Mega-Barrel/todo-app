
import os
from typing import List, Dict, Any

import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

FASTAPI_URL = os.getenv("FASTAPI_URL")

def refresh_ui():
    """Clears the cache and forces a rerun to refresh the todo list."""
    st.cache_data.clear()

@st.cache_data(show_spinner=False)
def get_todos() -> List[Dict[str, Any]]:
    """Fetches all todos from the FastAPI endpoint."""
    try:
        response = requests.get(f"{FASTAPI_URL}/todos", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to FastAPI backend. Ensure it is running at {FASTAPI_URL}: {e}")
        return []

def add_new_todo(title: str):
    """Sends a request to the API to create a new todo."""
    try:
        response = requests.post(f"{FASTAPI_URL}/todos", json={"title": title})
        response.raise_for_status()
        st.toast(f"Added: {title}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to add todo: {e}")
    refresh_ui()
    st.rerun()

def update_todo_status(todo_id: str, completed: bool):
    """Toggles the completion status of a todo."""
    try:
        response = requests.put(
            f"{FASTAPI_URL}/todos/{todo_id}",
            json={"completed": completed}
        )
        response.raise_for_status()
        st.toast("Status updated!" if completed else "Task marked as incomplete.")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to update status: {e}")
    refresh_ui()

def update_todo_title(todo_id: str, new_title: str, completed: bool):
    """Updates the title of a todo item."""
    try:
        response = requests.put(
            f"{FASTAPI_URL}/todos/{todo_id}",
            json={"title": new_title, "completed": completed}
        )
        response.raise_for_status()
        st.toast("Task edited successfully!")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to edit todo: {e}")
    refresh_ui()

def delete_todo_item(todo_id: str):
    """Sends a request to the API to delete a todo."""
    try:
        response = requests.delete(f"{FASTAPI_URL}/todos/{todo_id}")
        response.raise_for_status()
        st.toast("Todo deleted.")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to delete todo: {e}")
    refresh_ui()
