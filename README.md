# Simple FastAPI Project with PostgreSQL

A simple FastAPI application with Docker support that provides a REST API for managing items with PostgreSQL database integration.

## Features

- **FastAPI**: Modern, fast web framework for building APIs
- **PostgreSQL**: Robust relational database with SQLAlchemy ORM
- **Docker**: Containerized application for easy deployment
- **Health Check**: Built-in health check endpoint
- **CRUD Operations**: Create, Read, Update, Delete operations for items
- **Database Migrations**: Alembic for database schema management
- **AWS RDS Ready**: Configured to work with AWS RDS PostgreSQL

## AWS RDS PostgreSQL Setup

### Step 1: Create RDS PostgreSQL Instance

1. **Go to AWS RDS Console**
   - Navigate to AWS RDS in your AWS Console
   - Click "Create database"

2. **Configure Database**
   - Choose "PostgreSQL" as database engine
   - Select appropriate version (PostgreSQL 13+ recommended)
   - Choose instance class (db.t3.micro for testing)
   - Set database name: `fastapi_db`
   - Set master username and password
   - Note down the endpoint after creation

3. **Security Group Configuration**
   - Create/modify security group to allow connections on port 5432
   - Add inbound rule: Type: PostgreSQL, Port: 5432, Source: Your IP or 0.0.0.0/0 (for testing)

### Step 2: Configure Environment Variables

1. **Copy the example environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env file with your RDS credentials:**
   ```bash
   DATABASE_URL=postgresql://your_username:your_password@your-rds-endpoint.region.rds.amazonaws.com:5432/fastapi_db
   ```

   **Example:**
   ```bash
   DATABASE_URL=postgresql://myuser:mypassword@fastapi-db.cluster-abc123.us-east-1.rds.amazonaws.com:5432/fastapi_db
   ```

### Step 3: Test Database Connection

You can test the connection using psql:
```bash
psql "postgresql://your_username:your_password@your-rds-endpoint.region.rds.amazonaws.com:5432/fastapi_db"
```

## Environment Variables

Create a `.env` file in the project root:

```env
# For AWS RDS
DATABASE_URL=postgresql://username:password@your-rds-endpoint.region.rds.amazonaws.com:5432/database_name

# For local development (docker-compose will override this)
DATABASE_URL=postgresql://postgres:postgres123@localhost:5432/fastapi_db
```

## Running the Application

### Quick Start with Docker (AWS RDS)

1. **Set up your RDS connection:**
   ```bash
   # Edit .env file with your RDS credentials
   nano .env
   ```

2. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

   The application will:
   - Connect to your AWS RDS PostgreSQL instance
   - Run database migrations automatically
   - Start the FastAPI server on http://localhost:8000

### AWS EC2 Deployment

1. **Transfer files to EC2:**
   ```bash
   scp -i your-key.pem -r . ec2-user@your-ec2-instance:/home/ec2-user/fastapi-app/
   ```

2. **Connect to EC2 and run:**
   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-instance
   cd fastapi-app
   
   # Make sure Docker is installed and running
   sudo yum update -y
   sudo yum install -y docker
   sudo systemctl start docker
   sudo systemctl enable docker
   sudo usermod -a -G docker ec2-user
   
   # Install Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   
   # Run the application
   docker-compose up --build -d
   ```

### Local Development (without Docker)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your RDS credentials
   ```

3. **Run migrations and start app:**
   ```bash
   alembic upgrade head
   uvicorn main:app --reload
   ```

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check endpoint
- `GET /items` - Get all items (with pagination: `?skip=0&limit=100`)
- `GET /items/{item_id}` - Get specific item by ID
- `POST /items` - Create new item
- `PUT /items/{item_id}` - Update existing item
- `DELETE /items/{item_id}` - Delete item

## Accessing the Application

Once the application is running, you can access:

- **API**: http://localhost:8000
- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Example Usage

The application starts with sample data. Here are some example API calls:

### Get all items
```bash
curl http://localhost:8000/items
```

### Get specific item
```bash
curl http://localhost:8000/items/1
```

### Create a new item
```bash
curl -X POST "http://localhost:8000/items" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "New Laptop",
    "description": "High-performance gaming laptop",
    "price": 1299.99,
    "is_available": true
  }'
```

### Update an item
```bash
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Updated Laptop",
    "description": "Updated high-performance laptop",
    "price": 1099.99,
    "is_available": true
  }'
```

### Delete an item
```bash
curl -X DELETE http://localhost:8000/items/1
```

## Database Schema

The application uses PostgreSQL with the following table structure:

```sql
CREATE TABLE items (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    description VARCHAR,
    price FLOAT NOT NULL,
    is_available BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);
```

## Database Migrations

The project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback to previous migration
alembic downgrade -1
```

## Project Structure

```
fastapi-ec2-cicd/
├── main.py              # FastAPI application
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py              # Database operations
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose configuration
├── start.sh            # Application startup script
├── setup.sh            # Project setup script
├── alembic.ini         # Alembic configuration
├── alembic/            # Database migration files
├── .env.example        # Environment variables template
└── README.md           # This file
```

## Development

To extend this project:

1. **Add new endpoints**: Create new routes in `main.py`
2. **Add new models**: Create models in `models.py` and corresponding schemas in `schemas.py`
3. **Add database operations**: Implement CRUD operations in `crud.py`
4. **Add environment variables**: Update `.env.example` and `database.py`
5. **Database changes**: Create migrations with `alembic revision --autogenerate`

## Dependencies

- **FastAPI**: Web framework
- **SQLAlchemy**: Database ORM
- **PostgreSQL**: Database (psycopg2-binary driver)
- **Alembic**: Database migrations
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **python-dotenv**: Environment variables

## Deployment Considerations

### Security
- Use environment variables for sensitive data
- Enable HTTPS in production
- Use a non-root user in containers
- Keep dependencies updated

### Performance
- Use connection pooling
- Implement caching for frequently accessed data
- Monitor database performance
- Use proper indexing

### Monitoring
- Implement logging
- Add health checks
- Monitor database connections
- Set up alerts for failures

## License

This project is open source and available under the [MIT License](LICENSE).
