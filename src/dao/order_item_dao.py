# src/dao/order_item_dao.py
from typing import List, Dict
from src.config import get_supabase

class OrderItemDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_order_items(self, order_id: int, items: List[Dict]) -> None:
        """
        Insert multiple order items into the order_items table.
        Each item should be a dict with keys: prod_id, quantity, price
        """
        payloads = []
        for item in items:
            payloads.append({
                "order_id": order_id,
                "prod_id": item["prod_id"],
                "quantity": item["quantity"],
                "price": item["price"]  # price per item
            })

        if payloads:
            self._sb.table("order_items").insert(payloads).execute()

    def get_items_by_order(self, order_id: int) -> List[Dict]:
        """Fetch all items for a specific order"""
        resp = self._sb.table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []
