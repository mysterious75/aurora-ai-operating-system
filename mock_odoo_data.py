"""
Mock Odoo ERP Data for Aurora Office Furniture
Simulates realistic Australian office furniture business data
"""

from datetime import datetime, timedelta
import random

# Aurora's product catalog
PRODUCTS = [
    {"id": 1, "name": "ErgoPro Mesh Office Chair", "category": "Seating", "price": 449.00, "cost": 220.00, "stock": 45, "min_stock": 20},
    {"id": 2, "name": "Standing Desk Electric 160cm", "category": "Desks", "price": 899.00, "cost": 450.00, "stock": 12, "min_stock": 15},
    {"id": 3, "name": "Executive Leather Chair", "category": "Seating", "price": 1299.00, "cost": 650.00, "stock": 8, "min_stock": 10},
    {"id": 4, "name": "4-Drawer Filing Cabinet Steel", "category": "Storage", "price": 349.00, "cost": 180.00, "stock": 62, "min_stock": 25},
    {"id": 5, "name": "Conference Table 8-Seat", "category": "Tables", "price": 2199.00, "cost": 1100.00, "stock": 5, "min_stock": 3},
    {"id": 6, "name": "Monitor Arm Dual", "category": "Accessories", "price": 189.00, "cost": 85.00, "stock": 120, "min_stock": 50},
    {"id": 7, "name": "Cable Management Tray", "category": "Accessories", "price": 49.00, "cost": 22.00, "stock": 200, "min_stock": 80},
    {"id": 8, "name": "Ergonomic Keyboard Tray", "category": "Accessories", "price": 129.00, "cost": 60.00, "stock": 0, "min_stock": 30},
    {"id": 9, "name": "Acoustic Privacy Panel", "category": "Partitions", "price": 599.00, "cost": 300.00, "stock": 18, "min_stock": 10},
    {"id": 10, "name": "Mobile Pedestal 3-Drawer", "category": "Storage", "price": 279.00, "cost": 140.00, "stock": 55, "min_stock": 20},
    {"id": 11, "name": "Reception Desk L-Shape", "category": "Desks", "price": 1899.00, "cost": 950.00, "stock": 3, "min_stock": 5},
    {"id": 12, "name": "Task Chair Basic", "category": "Seating", "price": 199.00, "cost": 95.00, "stock": 150, "min_stock": 40},
    {"id": 13, "name": "Whiteboard 180x120cm", "category": "Accessories", "price": 159.00, "cost": 75.00, "stock": 35, "min_stock": 15},
    {"id": 14, "name": "CPU Holder Under-Desk", "category": "Accessories", "price": 79.00, "cost": 35.00, "stock": 0, "min_stock": 25},
    {"id": 15, "name": "Meeting Chair Stackable", "category": "Seating", "price": 149.00, "cost": 70.00, "stock": 90, "min_stock": 30},
]

# Canberra-based customers
CUSTOMERS = [
    {"id": 1, "name": "ACT Government Services", "type": "Government", "city": "Canberra", "state": "ACT", "credit_limit": 50000, "balance": 12450},
    {"id": 2, "name": "Capital Legal Partners", "type": "Corporate", "city": "Canberra", "state": "ACT", "credit_limit": 25000, "balance": 8900},
    {"id": 3, "name": "Queanbeyan City Council", "type": "Government", "city": "Queanbeyan", "state": "NSW", "credit_limit": 40000, "balance": 0},
    {"id": 4, "name": "Brindabella Business Park", "type": "Corporate", "city": "Canberra", "state": "ACT", "credit_limit": 30000, "balance": 22100},
    {"id": 5, "name": "ANU Research Centre", "type": "Education", "city": "Canberra", "state": "ACT", "credit_limit": 35000, "balance": 5600},
    {"id": 6, "name": "Sydney Tech Hub", "type": "Corporate", "city": "Sydney", "state": "NSW", "credit_limit": 45000, "balance": 18750},
    {"id": 7, "name": "Melbourne Co-Work Spaces", "type": "Corporate", "city": "Melbourne", "state": "VIC", "credit_limit": 20000, "balance": 15200},
    {"id": 8, "name": "Defence Housing Australia", "type": "Government", "city": "Canberra", "state": "ACT", "credit_limit": 60000, "balance": 31200},
    {"id": 9, "name": "Capital Health Medical", "type": "Healthcare", "city": "Canberra", "state": "ACT", "credit_limit": 28000, "balance": 7800},
    {"id": 10, "name": "Tuggeranong Office Solutions", "type": "Reseller", "city": "Canberra", "state": "ACT", "credit_limit": 15000, "balance": 14200},
]

def generate_orders():
    """Generate realistic order data"""
    orders = []
    status_options = ["draft", "confirmed", "delivered", "invoiced", "paid"]

    sample_orders = [
        {"customer_id": 1, "product_ids": [1, 6, 7], "qty": [20, 20, 20], "status": "invoiced", "days_ago": 45},
        {"customer_id": 2, "product_ids": [3, 5], "qty": [5, 1], "status": "confirmed", "days_ago": 3},
        {"customer_id": 4, "product_ids": [2, 6, 10], "qty": [8, 8, 8], "status": "delivered", "days_ago": 12},
        {"customer_id": 6, "product_ids": [1, 9], "qty": [30, 15], "status": "draft", "days_ago": 1},
        {"customer_id": 8, "product_ids": [12, 4, 10], "qty": [50, 20, 20], "status": "paid", "days_ago": 60},
        {"customer_id": 3, "product_ids": [11, 13], "qty": [2, 5], "status": "confirmed", "days_ago": 5},
        {"customer_id": 5, "product_ids": [1, 2, 6], "qty": [10, 10, 10], "status": "draft", "days_ago": 0},
        {"customer_id": 7, "product_ids": [15, 13], "qty": [40, 10], "status": "invoiced", "days_ago": 20},
        {"customer_id": 9, "product_ids": [3, 9], "qty": [3, 6], "status": "delivered", "days_ago": 8},
        {"customer_id": 10, "product_ids": [12, 7, 6], "qty": [25, 50, 25], "status": "confirmed", "days_ago": 2},
        {"customer_id": 1, "product_ids": [5, 15], "qty": [2, 30], "status": "draft", "days_ago": 0},
        {"customer_id": 4, "product_ids": [8, 14], "qty": [10, 10], "status": "draft", "days_ago": 0},  # Out of stock items!
    ]

    for i, order in enumerate(sample_orders, 1):
        customer = next(c for c in CUSTOMERS if c["id"] == order["customer_id"])
        products = [next(p for p in PRODUCTS if pid == p["id"]) for pid in order["product_ids"]]

        total = sum(p["price"] * q for p, q in zip(products, order["qty"]))
        date = datetime.now() - timedelta(days=order["days_ago"])

        orders.append({
            "id": i,
            "customer": customer["name"],
            "customer_type": customer["type"],
            "customer_city": customer["city"],
            "products": [p["name"] for p in products],
            "quantities": order["qty"],
            "total": total,
            "status": order["status"],
            "date": date.strftime("%Y-%m-%d"),
            "days_since_order": order["days_ago"],
        })

    return orders

def get_inventory_alerts():
    """Identify inventory issues"""
    alerts = []
    for p in PRODUCTS:
        if p["stock"] == 0:
            alerts.append({"type": "OUT_OF_STOCK", "severity": "CRITICAL", "product": p["name"], "category": p["category"]})
        elif p["stock"] < p["min_stock"]:
            alerts.append({"type": "LOW_STOCK", "severity": "HIGH", "product": p["name"], "current": p["stock"], "min": p["min_stock"]})
        elif p["stock"] > p["min_stock"] * 3:
            alerts.append({"type": "OVERSTOCK", "severity": "MEDIUM", "product": p["name"], "current": p["stock"], "min": p["min_stock"]})
    return alerts

def get_aging_receivables():
    """Get overdue invoices"""
    aging = []
    for c in CUSTOMERS:
        if c["balance"] > 0:
            utilization = (c["balance"] / c["credit_limit"]) * 100
            aging.append({
                "customer": c["name"],
                "balance": c["balance"],
                "credit_limit": c["credit_limit"],
                "utilization": round(utilization, 1),
                "risk": "HIGH" if utilization > 80 else "MEDIUM" if utilization > 50 else "LOW"
            })
    return sorted(aging, key=lambda x: x["utilization"], reverse=True)

def get_sales_summary():
    """Generate sales metrics"""
    orders = generate_orders()
    delivered = [o for o in orders if o["status"] in ["delivered", "invoiced", "paid"]]
    pending = [o for o in orders if o["status"] in ["draft", "confirmed"]]

    return {
        "total_revenue": sum(o["total"] for o in delivered),
        "pending_revenue": sum(o["total"] for o in pending),
        "total_orders": len(orders),
        "delivered_orders": len(delivered),
        "pending_orders": len(pending),
        "avg_order_value": round(sum(o["total"] for o in orders) / len(orders), 2),
        "top_customer": max(orders, key=lambda x: x["total"])["customer"],
    }

def get_dashboard_data():
    """Compile all data for AI analysis"""
    return {
        "products": PRODUCTS,
        "customers": CUSTOMERS,
        "orders": generate_orders(),
        "inventory_alerts": get_inventory_alerts(),
        "receivables": get_aging_receivables(),
        "sales_summary": get_sales_summary(),
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
