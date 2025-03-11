"""
Simple in-memory database for TODOs
"""
from typing import Dict, List
from uuid import UUID
from models import Todo, TodoCreate, TodoUpdate

class Database:
    """Simple in-memory database for TODOs"""
    def __init__(self):
        self.todos: Dict[UUID, Todo] = {}

    def get_todos(self) -> List[Todo]:
        """Get all TODOs"""
        return list(self.todos.values())

    def get_todo(self, todo_id: UUID) -> Todo | None:
        """Get a single TODO by ID"""
        return self.todos.get(todo_id)

    def create_todo(self, todo_create: TodoCreate) -> Todo:
        """Create a new TODO"""
        todo = Todo(
            id=todo_create.id,
            title=todo_create.title,
            description=todo_create.description,
            completed=todo_create.completed
        )
        self.todos[todo.id] = todo
        return todo

    def update_todo(self, todo_id: UUID, todo_update: TodoUpdate) -> Todo | None:
        """Update an existing TODO"""
        if todo_id not in self.todos:
            return None
        todo = self.todos[todo_id]
        if todo_update.title is not None:
            todo.title = todo_update.title
        if todo_update.description is not None:
            todo.description = todo_update.description
        if todo_update.completed is not None:
            todo.completed = todo_update.completed
        return todo

    def delete_todo(self, todo_id: UUID) -> bool:
        """Delete a TODO"""
        if todo_id not in self.todos:
            return False
        del self.todos[todo_id]
        return True

    def delete_all_todos(self) -> int:
        """Delete all TODOs and return the number of deleted items"""
        count = len(self.todos)
        self.todos.clear()
        return count

# Create a global instance of the database
db = Database()