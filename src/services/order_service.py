from typing import Optional, List, Dict
from dao.order_dao import OrderDAO
from dao.product_dao import ProductDAO
from dao.customer_dao import CustomerDAO

class OrderService:
    def __init__(self, order_dao: OrderDAO, product_dao: ProductDAO, customer_dao: CustomerDAO):
        self.order_dao = order_dao
        self.product_dao = product_dao
        self.customer_dao = customer_dao

    def place_order(self, cust_id: int, total_amount: float) -> Dict:
        if not cust_id:
            raise ValueError("Customer ID is required")
        if total_amount <= 0:
            raise ValueError("Order total must be greater than 0")

        # Use self.order_dao, not self.dao
        return self.order_dao.create_order(cust_id, total_amount)

    def get_order(self, order_id: int) -> Dict:
        if not order_id:
            raise ValueError("Order ID is required")

        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise LookupError(f"Order {order_id} not found")
        return order

    def update_status(self, order_id: int, status: str) -> Dict:
        if not order_id:
            raise ValueError("Order ID is required")
        if not status:
            raise ValueError("Order status is required")

        return self.order_dao.update_order_status(order_id, status)

    def cancel_order(self, order_id: int) -> Dict:
        if not order_id:
            raise ValueError("Order ID is required")

        return self.order_dao.delete_order(order_id)

    def list_orders(self, cust_id: Optional[int] = None) -> List[Dict]:
        return self.order_dao.list_orders(cust_id)
