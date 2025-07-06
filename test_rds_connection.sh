#!/bin/bash

# RDS Connection Test Script
set -e

echo "🔍 AWS RDS PostgreSQL Connection Test"
echo "======================================"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "❌ .env file not found!"
    echo "Please create .env file with your RDS credentials:"
    echo "DATABASE_URL=postgresql://username:password@your-rds-endpoint.region.rds.amazonaws.com:5432/database_name"
    exit 1
fi

# Load environment variables
source .env

if [ -z "$DATABASE_URL" ]; then
    echo "❌ DATABASE_URL not found in .env file!"
    exit 1
fi

echo "🔗 Testing connection to: $DATABASE_URL"

# Test connection using Python
python3 -c "
import psycopg2
import os
from urllib.parse import urlparse

try:
    # Parse the database URL
    url = urlparse(os.getenv('DATABASE_URL'))
    
    # Connect to the database
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    
    print('✅ Connection successful!')
    print(f'📊 PostgreSQL version: {version[0]}')
    
    cursor.close()
    conn.close()
    
except Exception as e:
    print(f'❌ Connection failed: {e}')
    print()
    print('Common issues:')
    print('1. Check if RDS instance is running')
    print('2. Verify security group allows connections on port 5432')
    print('3. Check if database credentials are correct')
    print('4. Ensure RDS instance is publicly accessible (if connecting from outside VPC)')
    exit(1)
"

echo "🎉 RDS connection test completed successfully!"
echo "You can now run: docker-compose up --build"
