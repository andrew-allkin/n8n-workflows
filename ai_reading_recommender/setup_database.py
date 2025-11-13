#!/usr/bin/env python3
"""
AI Reading Recommender - Database Setup Script
Creates the PostgreSQL database table for tracking reading recommendations.
"""

import psycopg2

# Database connection parameters (from docker-compose.yaml)
host = "localhost"
database = "n8n_workflows_data"
user = "admin"
password = "adminpassword"
port = "5432"

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

# Create table
print("Creating read_articles table...")
cursor.execute("""
CREATE TABLE IF NOT EXISTS read_articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    url VARCHAR(1000) NOT NULL UNIQUE,
    summary TEXT,
    source VARCHAR(200),
    content_type VARCHAR(50),
    subtopic VARCHAR(100),
    date_published TIMESTAMP,
    date_recommended TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_read TIMESTAMP,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    notes TEXT,
    author VARCHAR(200),
    reading_time_minutes INTEGER,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")
print("Table created")

# Create indexes
print("Creating indexes...")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_read_articles_url ON read_articles(url);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_read_articles_source ON read_articles(source);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_read_articles_content_type ON read_articles(content_type);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_read_articles_date_recommended ON read_articles(date_recommended);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_read_articles_is_read ON read_articles(is_read);")
print("Indexes created")

# Commit and close
conn.commit()
cursor.close()
conn.close()

print("Database setup completed successfully")
