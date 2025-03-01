import unittest
from database import init_db, create_order, get_order_status, update_order_status, get_all_orders, \
    get_db_connection


class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize the test database and create a sample order."""
        init_db()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM orders')
        conn.commit()
        conn.close()
        create_order('123', 'user1', ['item1', 'item2'], 100.0, 'Pending')


    def test_create_order(self):
        """Test creating an order."""
        create_order('456', 'user2', ['item3', 'item4'], 200.0, 'Pending')
        status = get_order_status('456')
        self.assertEqual(status, 'Pending')

    def test_update_order_status(self):
        """Test updating an order's status."""
        update_order_status('123', 'Completed')
        status = get_order_status('123')
        self.assertEqual(status, 'Completed')

    def test_get_all_orders(self):
        """Test retrieving all orders."""
        orders = get_all_orders()
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0][0], '123')  # order_id
        self.assertEqual(orders[0][4], 'Pending')  # status

if __name__ == '__main__':
    unittest.main()