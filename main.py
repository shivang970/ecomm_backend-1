from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import threading
from database import init_db, create_order, get_order_status, DATABASE_MAIN
from queue_processor import OrderQueue
from metrics import compute_metrics

app = FastAPI()
order_queue = OrderQueue()

# Initialize the main database
init_db()

# Start the queue processor in a separate thread
queue_processor_thread = threading.Thread(target=order_queue.process_orders)
queue_processor_thread.daemon = True
queue_processor_thread.start()

class OrderCreate(BaseModel):
    order_id: str
    user_id: str
    item_ids: List[str]
    total_amount: float

@app.post("/order")
async def create_order_endpoint(order: OrderCreate):
    order_id = order.order_id
    user_id = order.user_id
    item_ids = order.item_ids
    total_amount = order.total_amount

    create_order(order_id, user_id, item_ids, total_amount, status='Pending')
    order_queue.enqueue(order_id)
    return {"message": "Order created", "order_id": order_id}

@app.get("/order/{order_id}")
async def get_order_status_endpoint(order_id: str):
    status = get_order_status(order_id)
    if not status:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"order_id": order_id, "status": status}

@app.get("/metrics")
def get_metrics():
    metrics = compute_metrics()
    return metrics

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)