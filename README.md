# E-Commerce Order Management System

This is a backend system for managing and processing orders in an e-commerce platform. It provides RESTful APIs for order creation, status checking, and metrics reporting. The system uses **FastAPI** for the API, **SQLite** for the database, and an in-memory queue (`queue.Queue`) for asynchronous order processing.

---

## Features
- **Create Orders**: Submit orders with `user_id`, `order_id`, `item_ids`, and `total_amount`.
- **Check Order Status**: Retrieve the status of an order (`Pending`, `Processing`, `Completed`).
- **Metrics Reporting**: Get key metrics such as total orders, average processing time, and order status counts.
- **Asynchronous Processing**: Orders are processed asynchronously using an in-memory queue.

---

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ecommerce-backend.git
   cd ecommerce-backend

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
---

## Run the application
   ```bash
   uvicorn main:app --reload
```
---
## Run the tests
   ```bash
   set ENV=test
   ```
   ```bash
   python -m unittest discover tests -v
```

---
## Examples of API requests and responses using curl

1. Create Order: 
   
   Request
   ```bash
   curl -X POST "http://localhost:8000/order" \
   -H "Content-Type: application/json" \
   -d '{
     "order_id": "123",
     "user_id": "user1",
     "item_ids": ["item1", "item2"],
     "total_amount": 100.0
   }'
   ```
   Response
    ```
    {
     "message": "Order created",
     "order_id": "123"
   }
    ```

2. Get Order status:

   Request
   ```bash
   curl -X GET "http://localhost:8000/order/123"
   ```
   
   Response
   ```
   {
     "order_id": "123",
     "status": "Pending"
   }
   ```

3. Get Metrics:
   
   Request
   ```bash
   curl -X GET "http://localhost:8000/metrics"
   ```

   Response
   ```
   {
     "total_orders": 1,
     "average_processing_time": 0.0,
     "status_counts": {
       "Pending": 1,
       "Processing": 0,
       "Completed": 0
     }
   }
   ```
Note : 
- Replace localhost:8000 with your server's address if deployed elsewhere.
- Ensure the server is running before making requests.

---

## Design Decisions and Trade-offs
1. **Framework Choice: FastAPI**
   - Decision: FastAPI was chosen as the web framework.

   Reason:

   - FastAPI is modern, fast, and built for asynchronous programming, making it ideal for handling high concurrency.

   - It provides automatic OpenAPI documentation, which is useful for API exploration and testing.

   - Built-in support for Pydantic models ensures robust data validation and serialization.

   Trade-off:

   - FastAPI's asynchronous nature requires careful handling of blocking operations (e.g., database queries). Tools like threading.Lock and run_in_executor may be needed for thread safety.


2. **Database: SQLite**
   - Decision: SQLite was chosen as the database.

   Reason:

   - SQLite is lightweight, easy to set up, and requires no separate server process, making it ideal for prototyping and small-scale applications.

   - It supports ACID transactions, ensuring data consistency.

   Trade-off:

   - SQLite is not suitable for high-concurrency, large-scale applications. For production, a more robust database like PostgreSQL or MySQL would be better.


3. **In-Memory Queue: queue.Queue**

   - Decision: Python's queue.Queue was used for asynchronous order processing.

   Reason:

   - queue.Queue is simple, thread-safe, and fits well for in-memory queuing in a single-process application.

   - It allows decoupling of order creation and processing, simulating real-world asynchronous workflows.

   Trade-off:

   - The queue is in-memory, so it is not persistent. If the application crashes, pending orders in the queue will be lost.

   - For production, a distributed message queue like RabbitMQ or Kafka would be more reliable and scalable.


4. **Threading and Concurrency**

   - Decision: threading.Lock was used to ensure thread safety for shared resources (e.g., database and queue).

   Reason:

   - threading.Lock prevents race conditions when multiple threads access shared resources simultaneously.

   - It ensures that database operations and queue updates are atomic.

   Trade-off:

   - Locks can introduce performance bottlenecks if not used carefully. Overuse of locks can lead to deadlocks or reduced throughput.

   - For high-concurrency scenarios, asynchronous database libraries (e.g., asyncpg for PostgreSQL) or connection pooling would be more efficient.


5. **Metrics Computation**

   - Decision: Metrics are computed on-the-fly by querying the database.

   Reason:

   - This approach is simple and ensures that metrics are always up-to-date.

   - It avoids the need for additional storage or caching mechanisms.

   Trade-off:

   - Querying the database for metrics can be expensive for large datasets. For high-scale systems, pre-computed metrics or caching (e.g., Redis) would be more efficient.


6. **Scalability**

   - Decision: The system is designed to handle 1,000 concurrent orders.

   Reason:

   - FastAPI's asynchronous capabilities and Python's threading allow the system to handle moderate concurrency.

   - The use of queue.Queue and threading.Lock ensures thread safety and orderly processing.

   Trade-off:

   - The system is not horizontally scalable out-of-the-box. For higher loads, additional components like load balancers, distributed queues, and database replication would be needed.

---

## Assumptions
- **Order IDs are unique**: The system assumes that order_id is unique and provided by the client.

- **Fixed Processing Time**: The 5-second delay is a simplification; real-world processing times may vary.

- **Single-Process Application**: The system is designed to run as a single process. For production, multiple instances would be needed.

- **No Authentication/Authorization**: The system does not include user authentication or authorization for simplicity.
