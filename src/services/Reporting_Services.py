from typing import List, Dict
from dao.product_dao import ProductDAO
from dao.order_dao import OrderDAO
from dao.customer_dao import CustomerDAO
from dao.order_item_dao import OrderItemDAO  

class ReportingService:

    def __init__(self, product_dao, order_dao, customer_dao, order_item_dao):
        self.product_dao = product_dao
        self.order_dao = order_dao
        self.customer_dao = customer_dao
        self.order_item_dao = order_item_dao


    def top_selling_products(self, limit: int = 5) -> List[Dict]:
        """Compute top selling products based on order_items"""
        all_orders = self.order_dao.list_orders()
        product_count = {}

        for order in all_orders:
            order_id = order["order_id"]
            items = self.order_item_dao.get_items_by_order(order_id)
            for item in items:
                pid = item["prod_id"]
                qty = item["quantity"]
                product_count[pid] = product_count.get(pid, 0) + qty

        top_products = sorted(product_count.items(), key=lambda x: x[1], reverse=True)[:limit]

        result = []
        for pid, qty in top_products:
            product = self.product_dao.get_product_by_id(pid)
            if product:
                result.append({"product": product, "sold": qty})
        return result

    def total_revenue_last_month(self) -> float:
        all_orders = self.order_dao.list_orders()
        # Here you can filter by last month if needed
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
