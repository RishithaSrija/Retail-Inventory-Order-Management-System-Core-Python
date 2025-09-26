from typing import Optional, List, Dict
from src.config import get_supabase


class PaymentDAO:
    def __init__(self):
        self._sb = get_supabase()

    def create_payment(self, order_id: int, amount: float, method: str, status: str) -> Optional[Dict]:
        payload = {"order_id": order_id, "amount": amount, "method": method, "status": status}
        resp = self._sb.table("payments").insert(payload).execute()
        return resp.data[0] if resp.data else None

    def get_payment_by_id(self, payment_id: int) -> Optional[Dict]:
        resp = self._sb.table("payments").select("*").eq("payment_id", payment_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_payments(self, order_id: Optional[int] = None) -> List[Dict]:
        q = self._sb.table("payments").select("*").order("payment_id", desc=True)
        if order_id:
            q = q.eq("order_id", order_id)
        resp = q.execute()
        return resp.data or []
