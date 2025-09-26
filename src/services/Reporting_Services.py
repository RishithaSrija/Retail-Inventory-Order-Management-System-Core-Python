# src/services/reporting_service.py
from typing import List, Dict
from dao.product_dao import ProductDAO
from dao.order_dao import OrderDAO
from dao.customer_dao import CustomerDAO

class ReportingService:
    def __init__(self, product_dao: ProductDAO, order_dao: OrderDAO, customer_dao: CustomerDAO):
        self.product_dao = product_dao
        self.order_dao = order_dao
        self.customer_dao = customer_dao

    def top_selling_products(self, limit: int = 5) -> List[Dict]:
        all_orders = self.order_dao.list_orders()
        product_count = {}
        for order in all_orders:
            for item in order.get("items", []):
                pid = item["prod_id"]
                qty = item["quantity"]
                product_count[pid] = product_count.get(pid, 0) + qty

        # Sort by quantity sold
        top_products = sorted(product_count.items(), key=lambda x: x[1], reverse=True)[:limit]

        # Fetch product details
        result = []
        for pid, qty in top_products:
            product = self.product_dao.get_product_by_id(pid)
            if product:
                result.append({"product": product, "sold": qty})
        return result

    def total_revenue_last_month(self) -> float:
        all_orders = self.order_dao.list_orders()
        # Implement logic to filter last month and sum total_amount
        revenue = sum(o.get("total_amount", 0) for o in all_orders)
        return revenue

    def total_orders_per_customer(self) -> List[Dict]:
        all_orders = self.order_dao.list_orders()
        customer_count = {}
        for order in all_orders:
            cid = order.get("cust_id")
            customer_count[cid] = customer_count.get(cid, 0) + 1
        result = []
        for cid, count in customer_count.items():
            customer = self.customer_dao.get_customer_by_id(cid)
            if customer:
                result.append({"customer": customer, "orders": count})
        return result

    def frequent_customers(self, limit: int = 5) -> List[Dict]:
        all_orders = self.order_dao.list_orders()
        customer_count = {}
        for order in all_orders:
            cid = order.get("cust_id")
            customer_count[cid] = customer_count.get(cid, 0) + 1

        top_customers = sorted(customer_count.items(), key=lambda x: x[1], reverse=True)[:limit]
        result = []
        for cid, orders in top_customers:
            customer = self.customer_dao.get_customer_by_id(cid)
            if customer:
                result.append({"customer": customer, "orders": orders})
        return result
