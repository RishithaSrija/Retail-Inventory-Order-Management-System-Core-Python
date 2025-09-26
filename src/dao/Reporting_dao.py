from typing import List, Dict
from src.config import get_supabase


class ReportingDAO:
    def __init__(self):
        self._sb = get_supabase()
    def total_sales(self) -> float:
        resp = self._sb.rpc("total_sales").execute()
        return float(resp.data) if resp.data is not None else 0.0

    def sales_by_customer(self, cust_id: int) -> List[Dict]:
        resp = self._sb.rpc("sales_by_customer", {"cust_id": cust_id}).execute()
        return resp.data or []

    def sales_by_product(self, prod_id: int) -> List[Dict]:
        resp = self._sb.rpc("sales_by_product", {"prod_id": prod_id}).execute()
        return resp.data or []
