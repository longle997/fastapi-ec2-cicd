from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your models
from database import Base
import models

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.

def get_database_url():
    """Get database URL from environment or config"""
    from dotenv import load_dotenv
    load_dotenv()
    
    # First try to get from environment variable
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        print("Using DATABASE_URL from environment variable")
        return database_url
    
    # Fallback to config file
    config_url = config.get_main_option("sqlalchemy.url")
    if config_url and not config_url.startswith("postgresql://user:pass@localhost"):
        print("Using DATABASE_URL from alembic.ini config file")
        return config_url
    
    # If neither is properly set, raise an error
    raise ValueError(
        "DATABASE_URL not found. Please set the DATABASE_URL environment variable "
        "or update the sqlalchemy.url in alembic.ini with your database connection string."
    )

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = get_database_url()
    
    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
