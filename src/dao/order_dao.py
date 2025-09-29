from typing import Optional, List, Dict
from src.config import get_supabase

class OrderDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_order(self, cust_id: int, total_amount: float) -> Optional[Dict]:
        payload = {"cust_id": cust_id, "total_amount": total_amount}
        resp = self._sb.table("orders").insert(payload).execute()
        return resp.data[0] if resp.data else None

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        resp = self._sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None
    def get_items_by_order(self, order_id: int) -> List[Dict]:
        resp = self._sb.table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []

    def update_order_status(self, order_id: int, status: str) -> Optional[Dict]:
        self._sb.table("orders").update({"status": status}).eq("order_id", order_id).execute()
        resp = self._sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_order(self, order_id: int) -> Optional[Dict]:
        resp_before = self._sb.table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._sb.table("orders").delete().eq("order_id", order_id).execute()
        return row

    def list_orders(self, cust_id: Optional[int] = None) -> List[Dict]:
        q = self._sb.table("orders").select("*").order("order_id", desc=True)
        if cust_id:
            q = q.eq("cust_id", cust_id)
        resp = q.execute()
        return resp.data or []

    # Optional: for storing order items
    def create_order_items(self, order_id: int, items: List[Dict]):
     """Insert multiple items for an order including price"""
     for item in items:
        # Ensure 'price' exists in the item
        if "price" not in item:
            raise ValueError(f"Missing price for product ID {item['prod_id']}")
        payload = {
            "order_id": order_id,
            "prod_id": item["prod_id"],
            "quantity": item["quantity"],
            "price": item["price"]  # Insert price to satisfy NOT NULL constraint
        }
        self._sb.table("order_items").insert(payload).execute()
