
from typing import Optional, List, Dict
from src.config import get_supabase

class OrderRepository:
    def __init__(self):
        self._sb = get_supabase()

    def create_order(self, payload: Dict) -> Optional[Dict]:
        """
        Insert a new order and return the inserted row
        """
        self._sb.table("orders").insert(payload).execute()
        resp = self._sb.table("orders").select("*").eq("cust_id", payload["cust_id"]).order("order_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        resp = self._sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_orders_by_customer(self, customer_id: int) -> List[Dict]:
        resp = self._sb.table("orders").select("*").eq("cust_id", customer_id).order("order_id", desc=False).execute()
        return resp.data or []

    def update_order(self, order_id: int, fields: Dict) -> Optional[Dict]:
        self._sb.table("orders").update(fields).eq("order_id", order_id).execute()
        resp = self._sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    # ----------------- Order Items -----------------
    def add_order_item(self, order_id: int, prod_id: int, quantity: int, price: float) -> Optional[Dict]:
        payload = {
            "order_id": order_id,
            "prod_id": prod_id,
            "quantity": quantity,
            "price": price
        }
        self._sb.table("order_items").insert(payload).execute()
        resp = self._sb.table("order_items").select("*").eq("order_id", order_id).eq("prod_id", prod_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_order_items(self, order_id: int) -> List[Dict]:
        resp = self._sb.table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []
