#!/bin/bash

# Initialize Alembic for database migrations
echo "Initializing Alembic for database migrations..."

# Initialize alembic (only run once)
if [ ! -d "alembic" ]; then
    alembic init alembic
    echo "Alembic initialized."
else
    echo "Alembic already initialized."
fi

# Generate initial migration
echo "Generating initial migration..."
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
echo "Applying migrations..."
alembic upgrade head

echo "Database setup complete!"
