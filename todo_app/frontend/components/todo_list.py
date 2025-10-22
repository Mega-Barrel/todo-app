
from typing import List, Dict, Any

import streamlit as st
from api_client.todo_api import (
    update_todo_status,
    update_todo_title,
    delete_todo_item,
    add_new_todo
)

def display_todo_list(todos: List[Dict[str, Any]]):
    """Displays the list of todos with interactive elements."""
    st.markdown("---")

    if not todos:
        st.info("No tasks yet! Add one above. 🥳")
        return

    st.subheader("Your Tasks")

    if 'editing_id' not in st.session_state:
        st.session_state.editing_id = None

    for todo in todos:
        todo_id = todo["id"]
        title = todo["title"]
        completed = todo["completed"]

        col_title, col_edit, col_complete, col_delete = st.columns([4, 1, 1, 1])

        with col_title:
            if st.session_state.editing_id == todo_id:
                with st.form(f"edit_form_{todo_id}", clear_on_submit=False):
                    edited_title = st.text_input("Edit Task Title", value=title, label_visibility="collapsed")

                    col_save, col_cancel = st.columns(2)

                    if col_save.form_submit_button("Save"):
                        if edited_title:
                            update_todo_title(todo_id, edited_title, completed)
                            st.session_state.editing_id = None
                        else:
                            st.warning("Task title cannot be empty.")

                    if col_cancel.form_submit_button("Cancel"):
                        st.session_state.editing_id = None
                        st.rerun()
            else:
                if completed:
                    st.markdown(f"~~{title}~~", help="Task is completed.")
                else:
                    st.markdown(title)

        with col_edit:
            if st.session_state.editing_id is None:
                st.button(
                    "Edit",
                    key=f"edit_{todo_id}",
                    on_click=lambda id=todo_id: st.session_state.update(editing_id=id),
                    use_container_width=True
                )

        button_text = "Undo Complete" if completed else "Done"
        button_type = "secondary" if completed else "primary"

        with col_complete:
            st.button(
                button_text,
                key=f"complete_{todo_id}",
                on_click=update_todo_status,
                args=(todo_id, not completed),
                type=button_type,
                use_container_width=True
            )

        with col_delete:
            st.button(
                "Delete",
                key=f"delete_{todo_id}",
                on_click=delete_todo_item,
                args=(todo_id,),
                type="secondary",
                use_container_width=True
            )

        st.markdown("---")

def add_todo_form():
    """Form for adding new todo items."""

    with st.form("new_todo_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])

        new_title = col1.text_input("Enter a new task", label_visibility="collapsed", placeholder="What needs to be done?")
        submitted = col2.form_submit_button("Add Task", use_container_width=True, type="primary")

        if submitted and new_title:
            add_new_todo(new_title)
        elif submitted and not new_title:
            st.warning("Task title cannot be empty.")
