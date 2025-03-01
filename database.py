import os
import sqlite3
from datetime import datetime

# Database configuration
DATABASE_MAIN = 'orders.db'
DATABASE_TEST = 'test_orders.db'

def get_db_connection():
    """Get a connection to the specified database."""
    database_name = DATABASE_TEST if os.getenv('ENV', 'prod') == "test" else DATABASE_MAIN
    return sqlite3.connect(database_name)

def init_db():
    """Initialize the database schema."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            item_ids TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP NULL
        )
    ''')
    conn.commit()
    conn.close()

def create_order(order_id, user_id, item_ids, total_amount, status):
    """Create a new order in the specified database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO orders (order_id, user_id, item_ids, total_amount, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, user_id, str(item_ids), total_amount, status))
        conn.commit()
    finally:
        conn.close()

def get_order_status(order_id):
    """Get the status of an order from the specified database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT status FROM orders WHERE order_id = ?', (order_id,))
        result = cursor.fetchone()
    finally:
        conn.close()
    return result[0] if result else None

def update_order_status(order_id, status):
    """Update the status of an order in the specified database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        if status == "Completed":

            cursor.execute('''
                UPDATE orders SET status = ?, completed_at = ? WHERE order_id = ?
            ''', (status, datetime.utcnow().replace(microsecond=0), order_id))
        else:
            cursor.execute('''
                        UPDATE orders SET status = ? WHERE order_id = ?
                    ''', (status, order_id))
        conn.commit()
    finally:
        conn.close()

def get_all_orders():
    """Get all orders from the specified database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM orders')
        result = cursor.fetchall()
    finally:
        conn.close()
    return result