#!/usr/bin/env python3
"""
Text-to-SQL Agent - Database Setup Script
Creates PostgreSQL tables and loads data from CSV files.
"""

import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import os

# Database connection parameters (from docker-compose.yaml)
host = "localhost"
database = "n8n_workflows_data"
user = "admin"
password = "adminpassword"
port = 5432

# Connect to database
print("Connecting to database...")
conn = psycopg2.connect(
    host=host,
    database=database,
    user=user,
    password=password,
    port=port
)
cursor = conn.cursor()
print("Connected successfully")

# Drop existing tables
print("Dropping existing tables...")
cursor.execute("DROP TABLE IF EXISTS order_items CASCADE;")
cursor.execute("DROP TABLE IF EXISTS orders CASCADE;")
cursor.execute("DROP TABLE IF EXISTS products CASCADE;")
cursor.execute("DROP TABLE IF EXISTS customers CASCADE;")
print("Tables dropped")

# Create customers table
print("Creating customers table...")
cursor.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(50),
    state VARCHAR(2),
    country VARCHAR(50),
    created_at DATE
);
""")
print("Customers table created")

# Create products table
print("Creating products table...")
cursor.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10, 2) NOT NULL,
    stock_quantity INTEGER,
    supplier VARCHAR(100),
    sku VARCHAR(50) UNIQUE
);
""")
print("Products table created")

# Create orders table
print("Creating orders table...")
cursor.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20),
    shipping_address TEXT,
    payment_method VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);
""")
print("Orders table created")

# Create order_items table
print("Creating order_items table...")
cursor.execute("""
CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_unit DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
""")
print("Order_items table created")

# Commit table creation
conn.commit()

# Create SQLAlchemy engine for loading CSV data
database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(database_url)

# Get script directory for CSV files
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, 'data')

# Load customers data
print("Loading customers data...")
df = pd.read_csv(os.path.join(data_dir, 'customers.csv'))
df.to_sql('customers', engine, if_exists='append', index=False, method='multi')
print(f"Loaded {len(df)} customers")

# Load products data
print("Loading products data...")
df = pd.read_csv(os.path.join(data_dir, 'products.csv'))
df.to_sql('products', engine, if_exists='append', index=False, method='multi')
print(f"Loaded {len(df)} products")

# Load orders data
print("Loading orders data...")
df = pd.read_csv(os.path.join(data_dir, 'orders.csv'))
df.to_sql('orders', engine, if_exists='append', index=False, method='multi')
print(f"Loaded {len(df)} orders")

# Load order_items data
print("Loading order_items data...")
df = pd.read_csv(os.path.join(data_dir, 'order_items.csv'))
df.to_sql('order_items', engine, if_exists='append', index=False, method='multi')
print(f"Loaded {len(df)} order_items")

# Close connections
engine.dispose()
cursor.close()
conn.close()

print("Database setup completed successfully")
