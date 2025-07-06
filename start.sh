#!/bin/bash

# FastAPI Application Startup Script for AWS RDS
set -e

echo "🚀 Starting FastAPI application..."

# Load environment variables
if [ -f ".env" ]; then
    echo "📋 Loading environment variables from .env file..."
    export $(cat .env | grep -v '^#' | xargs)
fi

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Start the FastAPI application
echo "✅ Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8000
