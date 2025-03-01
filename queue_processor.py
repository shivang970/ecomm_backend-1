import queue
import time
import threading
from database import update_order_status

class OrderQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.lock = threading.Lock()

    def enqueue(self, order_id):
        with self.lock:
            self.queue.put(order_id)

    def process_orders(self):
        while True:
            if not self.queue.empty():
                with self.lock:
                    order_id = self.queue.get()
                self._process_order(order_id)
            time.sleep(1)  # Simulate processing delay

    def _process_order(self, order_id):
        # Simulate order processing
        update_order_status(order_id, 'Processing')
        time.sleep(5)  # Simulate processing time
        update_order_status(order_id, 'Completed')