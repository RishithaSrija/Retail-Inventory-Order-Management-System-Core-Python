# src/dao/payment_dao.py
from typing import Optional, Dict
from src.config import get_supabase

class PaymentDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_payment(self, order_id: int, amount: float, method: str | None, status: str) -> Optional[Dict]:
        """Insert a new payment record"""
        payload = {"order_id": order_id, "amount": amount, "method": method, "status": status}
        resp = self._sb.table("payments").insert(payload).execute()
        return resp.data[0] if resp.data else None

    def get_payment_by_order(self, order_id: int) -> Optional[Dict]:
        """Retrieve payment by order ID"""
        resp = self._sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_payment(self, payment_id: int, fields: Dict) -> Optional[Dict]:
        """Update payment fields (status, method, etc.)"""
        self._sb.table("payments").update(fields).eq("payment_id", payment_id).execute()
        # Return the updated row
        resp = self._sb.table("payments").select("*").eq("payment_id", payment_id).limit(1).execute()
        return resp.data[0] if resp.data else None
