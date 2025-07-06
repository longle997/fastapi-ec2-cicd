#!/bin/bash

# Setup script for initializing the FastAPI PostgreSQL project
set -e

echo "🚀 Setting up FastAPI PostgreSQL project..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "✅ Created .env file. Please update it with your database credentials."
fi

# Install Python dependencies (if running locally)
if [ "$1" = "local" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
    
    # Initialize Alembic if not already done
    if [ ! -d "alembic/versions" ] || [ -z "$(ls -A alembic/versions)" ]; then
        echo "🔄 Initializing database migrations..."
        alembic revision --autogenerate -m "Initial migration"
    fi
    
    # Apply migrations
    echo "🔧 Applying database migrations..."
    alembic upgrade head
    
    echo "✅ Local setup complete!"
    echo "🚀 You can now run: uvicorn main:app --reload"
else
    echo "🐳 For Docker setup, run: docker-compose up --build"
fi

echo "📖 Check README.md for more details!"
