import pytest
from app.models import TodoCreate

def test_create_todo(client):
    """Test creating a todo."""
    # Create todo data
    todo_data = {
        "title": "Test Todo",
        "description": "This is a test todo",
        "completed": False
    }

    # Send POST request to create todo
    response = client.post("/api/todos/", json=todo_data)

    # Check response
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == todo_data["title"]
    assert data["description"] == todo_data["description"]
    assert data["completed"] == todo_data["completed"]
    assert "id" in data
    assert "created_at" in data

def test_read_todos(client):
    """Test reading all todos."""
    # Create a todo first
    todo_data = {"title": "Test Todo"}
    client.post("/api/todos/", json=todo_data)

    # Send GET request to read todos
    response = client.get("/api/todos/")

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_read_todo(client):
    """Test reading a specific todo."""
    # Create a todo first
    todo_data = {"title": "Test Todo"}
    create_response = client.post("/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]

    # Send GET request to read todo
    response = client.get(f"/api/todos/{todo_id}")

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == todo_data["title"]

def test_update_todo(client):
    """Test updating a todo."""
    # Create a todo first
    todo_data = {"title": "Test Todo"}
    create_response = client.post("/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]

    # Update data
    update_data = {
        "title": "Updated Todo",
        "description": "This todo has been updated",
        "completed": True
    }

    # Send PUT request to update todo
    response = client.put(f"/api/todos/{todo_id}", json=update_data)

    # Check response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert data["completed"] == update_data["completed"]

def test_delete_todo(client):
    """Test deleting a todo."""
    # Create a todo first
    todo_data = {"title": "Test Todo"}
    create_response = client.post("/api/todos/", json=todo_data)
    todo_id = create_response.json()["id"]

    # Send DELETE request to delete todo
    response = client.delete(f"/api/todos/{todo_id}")

    # Check response
    assert response.status_code == 204

    # Verify todo is deleted
    get_response = client.get(f"/api/todos/{todo_id}")
    assert get_response.status_code == 404
