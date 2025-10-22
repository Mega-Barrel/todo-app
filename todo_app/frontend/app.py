
"""
Entry Point to Streamlit App
"""

import streamlit as st
from components.todo_list import (
    add_todo_form,
    display_todo_list
)
from api_client.todo_api import get_todos

def main():
    """Main function to run the Streamlit application."""

    st.set_page_config(layout="centered", page_title="Streamlit + FastAPI Todo App")

    st.title("Streamlit/FastAPI Todo App 🚀")
    st.markdown("""
        <p style="font-size: small; color: gray;">
        Backend powered by FastAPI on port 8000 (Ensure it is running!).
        </p>
    """, unsafe_allow_html=True)

    add_todo_form()

    todos = get_todos()
    display_todo_list(todos)

if __name__ == "__main__":
    main()
