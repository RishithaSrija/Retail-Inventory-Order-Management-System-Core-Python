from typing import Optional, List, Dict
from dao.order_dao import OrderDAO
from dao.product_dao import ProductDAO
from dao.customer_dao import CustomerDAO

class OrderError(Exception):
    pass

class OrderService:
    def __init__(self, order_dao: OrderDAO, product_dao: ProductDAO, customer_dao: CustomerDAO):
        self.order_dao = order_dao
        self.product_dao = product_dao
        self.customer_dao = customer_dao

    # def create_order(self, cust_id: int, items: List[Dict]) -> Dict:
    #  """Create an order with multiple items"""
    #  if not cust_id:
    #     raise OrderError("Customer ID is required")
    #  if not items:
    #     raise OrderError("Order must have at least one item")

    #  total_amount = 0
    # # Calculate total and validate items
    #  for item in items:
    #     product = self.product_dao.get_product_by_id(item["prod_id"])
    #     if not product:
    #         raise OrderError(f"Product ID {item['prod_id']} not found")
    #     if item["quantity"] <= 0:
    #         raise OrderError("Quantity must be greater than 0")
    #     # Compute total
    #     total_amount += product["price"] * item["quantity"]
    #     # Attach price to item for order_items insertion
    #     item["price"] = product["price"]

    #  # Create order
    #  order = self.order_dao.create_order(cust_id, total_amount)

    # # Insert order items with price
    #  if hasattr(self.order_dao, "create_order_items"):
    #     self.order_dao.create_order_items(order["order_id"], items)

    #  return order
    def create_order(self, cust_id: int, items: List[Dict]) -> Dict:
     """Create an order with multiple items"""
     if not cust_id:
        raise OrderError("Customer ID is required")
     if not items:
        raise OrderError("Order must have at least one item")

    # Calculate total amount and prepare items with price
     total_amount = 0
     items_with_price = []
     for item in items:
        product = self.product_dao.get_product_by_id(item["prod_id"])
        if not product:
            raise OrderError(f"Product ID {item['prod_id']} not found")
        if item["quantity"] <= 0:
            raise OrderError("Quantity must be greater than 0")

        price = product["price"]
        total_amount += price * item["quantity"]

        items_with_price.append({
            "prod_id": item["prod_id"],
            "quantity": item["quantity"],
            "price": price
        })

    # Create order in DB
     order = self.order_dao.create_order(cust_id, total_amount)

    # Add order items to order_items table
     if hasattr(self.order_dao, "create_order_items"):
        self.order_dao.create_order_items(order["order_id"], items_with_price)

     return order



    def get_order_details(self, order_id: int) -> Dict:
        order = self.order_dao.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order {order_id} not found")
        return order

    def update_order_status(self, order_id: int, status: str) -> Dict:
        return self.order_dao.update_order_status(order_id, status)

    def cancel_order(self, order_id: int) -> Dict:
        return self.order_dao.delete_order(order_id)

    def list_orders(self, cust_id: Optional[int] = None) -> List[Dict]:
        return self.order_dao.list_orders(cust_id)
