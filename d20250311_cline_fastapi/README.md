# FastAPI TODO API

A simple TODO API built with FastAPI and SQLAlchemy, using uv as the package manager.

## Features

- Create, read, update, and delete TODO items
- SQLite database for data storage
- Automatic API documentation with Swagger UI
- Comprehensive test suite

## Requirements

- Python 3.8+
- uv package manager

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install uv (if not already installed):

```bash
pip install uv
```

3. Create a virtual environment and install dependencies:

```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

## Usage

1. Start the server:

```bash
uvicorn app.main:app --reload
```

2. Open your browser and navigate to:
   - API: http://localhost:8000/
   - API Documentation: http://localhost:8000/docs
   - Alternative API Documentation: http://localhost:8000/redoc

## API Endpoints

- `GET /api/todos/`: List all todos
- `POST /api/todos/`: Create a new todo
- `GET /api/todos/{id}`: Get a specific todo
- `PUT /api/todos/{id}`: Update a todo
- `DELETE /api/todos/{id}`: Delete a todo

## Example

### Create a new TODO

```bash
curl -X POST "http://localhost:8000/api/todos/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Buy groceries", "description": "Milk, eggs, bread", "completed": false}'
```

### Get all TODOs

```bash
curl -X GET "http://localhost:8000/api/todos/"
```

## Testing

Run tests using pytest:

```bash
pytest app/tests/
```

## License

MIT
