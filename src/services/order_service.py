from typing import List, Dict

from src.dao.customer_dao import CustomerRepository
from src.dao.product_dao import ProductRepository
from src.dao.order_dao import OrderRepository  # You'll create this DAO
from decimal import Decimal


class OrderError(Exception):

    def __init__(self):
     self.cust_repo=CustomerRepository()
     self.prod_repo=ProductRepository()
     self.order_repo=OrderRepository()


    def create_order(self,customer_id: int,list_prod :List[Dict[str,int]]):
       
        customer=self.customer_repo.get_customer_by_id(customer_id)
        if not customer:
          raise OrderError(f"Customer not found {customer_id}")
        total_amount=Decimal("0.0")
        updated_pros=[]
        for item in list_prod:
          prod=self.prod_repo.get_product_by_id(item["prod_id"])
          if not prod:
             raise OrderError(f"Product not found: {item['prod_id']}")
          if prod.get("stock",0)<item["quantity"]:
             raise OrderError (f"No enough stock for the product: {prod['name']}")
          total_amount+=Decimal(prod['price'])*item['quantity']
          updated_pros.append((prod,item['quantity']))

        for prod, qty in updated_pros:
            new_stock = (prod["stock"] or 0) - qty
            self.product_repo.update_product(prod["prod_id"], {"stock": new_stock})

        # Insert order
        order_payload = {
            "cust_id": customer_id,
            "total_amount": float(total_amount),
            "status": "PLACED"
        }
        order = self.order_repo.create_order(order_payload)

        # Insert order items
        for prod, qty in updated_pros:
            self.order_repo.add_order_item(order["order_id"], prod["prod_id"], qty, prod["price"])

        return self.get_order_details(order["order_id"])

    def get_order_details(self, order_id: int) -> Dict:
        """
        Fetch full order details (order + customer + items)
        """
        order = self.order_repo.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order not found: {order_id}")

        customer = self.customer_repo.get_customer_by_id(order["cust_id"])
        items = self.order_repo.get_order_items(order_id)
        return {"order": order, "customer": customer, "items": items}

    def list_orders_by_customer(self, customer_id: int) -> List[Dict]:
        """
        List all orders of a customer
        """
        return self.order_repo.list_orders_by_customer(customer_id)

    def cancel_order(self, order_id: int) -> Dict:
        """
        Cancel order if status = PLACED
        Restore stock
        """
        order = self.order_repo.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order not found: {order_id}")
        if order["status"] != "PLACED":
            raise OrderError("Only PLACED orders can be cancelled")

        items = self.order_repo.get_order_items(order_id)
        for item in items:
            prod = self.product_repo.get_product_by_id(item["prod_id"])
            self.product_repo.update_product(prod["prod_id"], {"stock": prod["stock"] + item["quantity"]})

        self.order_repo.update_order(order_id, {"status": "CANCELLED"})
        return self.get_order_details(order_id)

    def complete_order(self, order_id: int) -> Dict:
        """
        Mark order as COMPLETED
        """
        order = self.order_repo.get_order_by_id(order_id)
        if not order:
            raise OrderError(f"Order not found: {order_id}")
        if order["status"] != "PLACED":
            raise OrderError("Only PLACED orders can be completed")

        self.order_repo.update_order(order_id, {"status": "COMPLETED"})
        return self.get_order_details(order_id)

                      
