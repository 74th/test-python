#!/bin/bash

# 仮想環境を有効化する
source .venv/bin/activate

# FastAPIアプリケーションを起動する
echo "Starting FastAPI application on http://localhost:8000"
echo "API documentation available at http://localhost:8000/docs"
uvicorn main:app --reload --host 0.0.0.0 --port 8000