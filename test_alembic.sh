#!/bin/bash

# Test Alembic configuration with environment variables
set -e

echo "🧪 Testing Alembic configuration with environment variables..."

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found. Please create one with DATABASE_URL"
    echo "   Example: DATABASE_URL=postgresql://user:password@host:port/database"
    exit 1
fi

# Load environment variables
echo "📋 Loading environment variables from .env file..."
export $(cat .env | grep -v '^#' | grep -v '^$' | xargs)

# Check if DATABASE_URL is set
if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not set in environment variables"
    echo "   Please add DATABASE_URL to your .env file"
    exit 1
fi

echo "✅ DATABASE_URL found: ${DATABASE_URL}"

# Test Alembic configuration
echo "🔍 Testing Alembic configuration..."
alembic check

# Show current migration status
echo "📊 Current migration status:"
alembic current

# Show migration history
echo "📚 Migration history:"
alembic history

echo "✅ Alembic configuration test completed successfully!"
