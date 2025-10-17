#!/usr/bin/env python3
"""
Script to create PostgreSQL tables and load data from CSV files.
Connects to the local PostgreSQL database running in Docker.
"""

import psycopg2
from psycopg2 import sql
import pandas as pd
from sqlalchemy import create_engine
import os

# Database connection parameters (hardcoded from docker-compose.yaml)
DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'test',
    'user': 'admin',
    'password': 'adminpassword'
}

# SQLAlchemy connection string
DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"

def get_connection():
    """Create and return a database connection."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✓ Successfully connected to PostgreSQL database")
        return conn
    except Exception as e:
        print(f"✗ Error connecting to database: {e}")
        raise

def create_tables(cursor):
    """Create all tables with proper schema and constraints."""
    
    print("\nCreating tables...")
    
    # Drop existing tables (in reverse order of dependencies)
    drop_tables = """
    DROP TABLE IF EXISTS order_items CASCADE;
    DROP TABLE IF EXISTS orders CASCADE;
    DROP TABLE IF EXISTS products CASCADE;
    DROP TABLE IF EXISTS customers CASCADE;
    """
    cursor.execute(drop_tables)
    print("✓ Dropped existing tables (if any)")
    
    # Create customers table
    create_customers = """
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
    """
    cursor.execute(create_customers)
    print("✓ Created customers table")
    
    # Create products table
    create_products = """
    CREATE TABLE products (
        product_id INTEGER PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        category VARCHAR(50),
        price DECIMAL(10, 2) NOT NULL,
        stock_quantity INTEGER,
        supplier VARCHAR(100),
        sku VARCHAR(50) UNIQUE
    );
    """
    cursor.execute(create_products)
    print("✓ Created products table")
    
    # Create orders table
    create_orders = """
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
    """
    cursor.execute(create_orders)
    print("✓ Created orders table")
    
    # Create order_items table
    create_order_items = """
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
    """
    cursor.execute(create_order_items)
    print("✓ Created order_items table")

def load_csv_data(engine, csv_file, table_name):
    """Load data from CSV file into the specified table using pandas."""
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'data', csv_file)
    
    try:
        # Read CSV with pandas
        df = pd.read_csv(csv_path)
        
        # Use pandas to_sql method for efficient bulk insert
        row_count = len(df)
        df.to_sql(table_name, engine, if_exists='append', index=False, method='multi')
        
        print(f"✓ Loaded {row_count} records into {table_name}")
            
    except FileNotFoundError:
        print(f"✗ Error: Could not find {csv_file}")
        raise
    except Exception as e:
        print(f"✗ Error loading data into {table_name}: {e}")
        raise

def verify_data(cursor):
    """Verify the data was loaded correctly."""
    
    print("\nVerifying data...")
    
    tables = ['customers', 'products', 'orders', 'order_items']
    
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"  {table}: {count} records")
    
    # Test a join query to verify relationships
    print("\nTesting relationships with sample query:")
    test_query = """
    SELECT 
        c.name as customer_name,
        o.order_id,
        o.order_date,
        COUNT(oi.order_item_id) as items_count,
        o.total_amount
    FROM customers c
    JOIN orders o ON c.customer_id = o.customer_id
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE c.customer_id = 1
    GROUP BY c.name, o.order_id, o.order_date, o.total_amount
    ORDER BY o.order_date
    LIMIT 5;
    """
    
    cursor.execute(test_query)
    results = cursor.fetchall()
    
    print("\n  Sample: Orders for customer 1:")
    print("  " + "-" * 70)
    for row in results:
        print(f"  {row[0]:20} | Order #{row[1]} | {row[2]} | {row[3]} items | ${row[4]}")

def main():
    """Main execution function."""
    
    print("=" * 70)
    print("PostgreSQL Database Setup Script")
    print("=" * 70)
    
    conn = None
    engine = None
    try:
        # Connect to database with psycopg2 for table creation
        conn = get_connection()
        cursor = conn.cursor()
        
        # Create tables
        create_tables(cursor)
        conn.commit()
        
        # Create SQLAlchemy engine for pandas
        print("\nCreating SQLAlchemy engine for data loading...")
        engine = create_engine(DATABASE_URL)
        print("✓ SQLAlchemy engine created")
        
        # Load data in order (respecting foreign key constraints)
        print("\nLoading data from CSV files...")
        load_csv_data(engine, 'customers.csv', 'customers')
        load_csv_data(engine, 'products.csv', 'products')
        load_csv_data(engine, 'orders.csv', 'orders')
        load_csv_data(engine, 'order_items.csv', 'order_items')
        
        print("\n✓ All data loaded successfully")
        
        # Verify data
        verify_data(cursor)
        
        print("\n" + "=" * 70)
        print("✓ Database setup completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"\n✗ Error occurred. All changes rolled back: {e}")
        raise
        
    finally:
        if engine:
            engine.dispose()
        if conn:
            conn.close()
            print("\n✓ Database connection closed")

if __name__ == "__main__":
    main()

