from database import get_all_orders
from datetime import datetime

def compute_metrics():
    """Compute metrics for the specified database."""
    orders = get_all_orders()
    total_orders = len(orders)
    status_counts = {'Pending': 0, 'Processing': 0, 'Completed': 0}
    total_processing_time = 0
    completed_orders = 0

    for order in orders:
        status_counts[order[4]] += 1
        if order[4] == 'Completed':
            print(order[5])
            created_at = datetime.strptime(order[5], '%Y-%m-%d %H:%M:%S')
            completed_at = datetime.strptime(order[6], '%Y-%m-%d %H:%M:%S')
            total_processing_time += (completed_at - created_at).total_seconds()
            completed_orders += 1
            print(f"{created_at} - {completed_at} - {total_processing_time}")

    avg_processing_time = total_processing_time / completed_orders if completed_orders > 0 else 0

    return {
        "total_orders": total_orders,
        "average_processing_time": avg_processing_time,
        "status_counts": status_counts
    }