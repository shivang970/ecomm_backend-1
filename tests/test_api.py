import unittest
from datetime import datetime

import requests
from fastapi.testclient import TestClient
from main import app
from database import init_db, get_db_connection, DATABASE_TEST


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the test database and start the FastAPI test client."""
        # Initialize the test database
        init_db()

        # Start the FastAPI test client
        cls.client = TestClient(app)

    def setUp(self):
        """Ensure the test database is clean before each test."""
        # Clear all orders from the test database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM orders')
        conn.commit()
        conn.close()

    def test_create_order(self):
        """Test creating an order via the API."""
        response = self.client.post(
            "/order",
            json={
                "order_id": "123",
                "user_id": "user1",
                "item_ids": ["item1", "item2"],
                "total_amount": 100.0
            }
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Order created", "order_id": "123"})

    def test_get_order_status(self):
        """Test retrieving the status of an order via the API."""
        # Create an order first
        self.client.post(
            "/order",
            json={
                "order_id": "123",
                "user_id": "user1",
                "item_ids": ["item1", "item2"],
                "total_amount": 100.0
            }
        )

        # Check the order status
        response = self.client.get("/order/123")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"order_id": "123", "status": "Pending"})

    def test_get_metrics(self):
        """Test retrieving metrics via the API."""
        # Create an order first
        self.client.post(
            "/order",
            json={
                "order_id": "123",
                "user_id": "user1",
                "item_ids": ["item1", "item2"],
                "total_amount": 100.0
            }
        )

        # Wait for the order to be processed (simulate processing time)
        import time
        time.sleep(6)
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
                    UPDATE orders SET status = ?, completed_at = ? WHERE order_id = ?
                ''', ("Completed", datetime.utcnow().replace(microsecond=0), "123"))
        conn.commit()
        conn.close()
        # Check the metrics
        response = self.client.get("/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "total_orders": 1,
            "average_processing_time": 6.0,
            "status_counts": {
                "Pending": 0,
                "Processing": 0,
                "Completed": 1
            }
        })

if __name__ == '__main__':
    unittest.main()