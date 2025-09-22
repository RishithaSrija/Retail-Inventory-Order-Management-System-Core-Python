from typing import Optional, Dict, List
from src.config import get_supabase

class PaymentRepository:
    def __init__(self):
        self._sb = get_supabase()

    def create_payment(self, order_id: int, amount: float) -> Dict:
        payload = {
            "order_id": order_id,
            "amount": amount,
            "status": "PENDING",
            "method": None
        }
        self._sb.table("payments").insert(payload).execute()
        resp = self._sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def process_payment(self, order_id: int, method: str) -> Optional[Dict]:
        self._sb.table("payments").update({"status": "PAID", "method": method}).eq("order_id", order_id).execute()
        resp = self._sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def refund_payment(self, order_id: int) -> Optional[Dict]:
        self._sb.table("payments").update({"status": "REFUNDED"}).eq("order_id", order_id).execute()
        resp = self._sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_payment_by_order(self, order_id: int) -> Optional[Dict]:
        resp = self._sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None
