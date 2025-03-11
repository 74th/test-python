"""
Tests for the FastAPI TODO application
"""
import uuid
from fastapi.testclient import TestClient
from main import app
from database import db

client = TestClient(app)


def test_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the TODO API"}


def test_create_todo():
    """Test creating a new TODO"""
    # Clear the database before testing
    db.todos.clear()

    todo_data = {
        "title": "Test TODO",
        "description": "This is a test TODO",
        "completed": False
    }

    response = client.post("/todos", json=todo_data)

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] == todo_data["completed"]
    assert "id" in data


def test_get_todos():
    """Test getting all TODOs"""
    # Clear the database and add a test TODO
    db.todos.clear()

    todo_data = {
        "title": "Test TODO",
        "description": "This is a test TODO",
        "completed": False
    }

    create_response = client.post("/todos", json=todo_data)

    response = client.get("/todos")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["title"] == todo_data["title"]


def test_get_todo():
    """Test getting a single TODO by ID"""
    # Clear the database and add a test TODO
    db.todos.clear()

    todo_data = {
        "title": "Test TODO",
        "description": "This is a test TODO",
        "completed": False
    }

    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    response = client.get(f"/todos/{todo_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["id"] == todo_id


def test_get_todo_not_found():
    """Test getting a non-existent TODO"""
    non_existent_id = str(uuid.uuid4())
    response = client.get(f"/todos/{non_existent_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_update_todo():
    """Test updating a TODO"""
    # Clear the database and add a test TODO
    db.todos.clear()

    todo_data = {
        "title": "Test TODO",
        "description": "This is a test TODO",
        "completed": False
    }

    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    update_data = {
        "title": "Updated TODO",
        "completed": True
    }

    response = client.put(f"/todos/{todo_id}", json=update_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["completed"] == update_data["completed"]
    # Description should remain unchanged
    assert data["description"] == todo_data["description"]


def test_update_todo_not_found():
    """Test updating a non-existent TODO"""
    non_existent_id = str(uuid.uuid4())
    update_data = {
        "title": "Updated TODO",
        "completed": True
    }

    response = client.put(f"/todos/{non_existent_id}", json=update_data)

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_todo():
    """Test deleting a TODO"""
    # Clear the database and add a test TODO
    db.todos.clear()

    todo_data = {
        "title": "Test TODO",
        "description": "This is a test TODO",
        "completed": False
    }

    create_response = client.post("/todos", json=todo_data)
    todo_id = create_response.json()["id"]

    response = client.delete(f"/todos/{todo_id}")

    assert response.status_code == 204

    # Verify the TODO is deleted
    get_response = client.get(f"/todos/{todo_id}")
    assert get_response.status_code == 404


def test_delete_todo_not_found():
    """Test deleting a non-existent TODO"""
    non_existent_id = str(uuid.uuid4())
    response = client.delete(f"/todos/{non_existent_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_delete_all_todos():
    """Test deleting all TODOs"""
    # Clear the database and add multiple TODOs
    db.todos.clear()

    # Create 3 TODOs
    for i in range(3):
        todo_data = {
            "title": f"Test TODO {i}",
            "description": f"This is test TODO {i}",
            "completed": False
        }
        client.post("/todos", json=todo_data)

    # Verify 3 TODOs exist
    get_response = client.get("/todos")
    assert len(get_response.json()) == 3

    # Delete all TODOs
    response = client.delete("/todos")

    assert response.status_code == 200
    data = response.json()
    assert data["deleted_count"] == 3
    assert "3 TODOs have been deleted" in data["message"]

    # Verify all TODOs are deleted
    get_response = client.get("/todos")
    assert len(get_response.json()) == 0


def test_delete_all_todos_when_empty():
    """Test deleting all TODOs when the database is empty"""
    # Clear the database
    db.todos.clear()

    # Delete all TODOs
    response = client.delete("/todos")

    assert response.status_code == 200
    data = response.json()
    assert data["deleted_count"] == 0
    assert "0 TODOs have been deleted" in data["message"]