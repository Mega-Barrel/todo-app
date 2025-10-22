"""
FastAPI Entry Point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import todo as todo_router

def get_application() -> FastAPI:
    """Initializes and configures the FastAPI application."""
    app = FastAPI(
        title="FastAPI Todo List (Refactored)",
        description="A scalable CRUD API for managing a Todo list backed by SQLite.",
        version="1.0.0"
    )

    # Middleware setup (same as before)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(todo_router.router, prefix="/api/v1")

    @app.get("/", tags=["Root"])
    def read_root():
        """Health check endpoint."""
        return {"message": "Welcome to the FastAPI Todo API"}
    return app

app = get_application()
