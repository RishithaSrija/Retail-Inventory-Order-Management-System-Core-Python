# src/dao/customer_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class CustomerDAO:
    """Data Access Object for Customer entity"""

    def __init__(self):
        self._sb = get_supabase()

    def create_customer(self, name: str, email: str, phone: str | None = None, city: str | None = None) -> Optional[Dict]:
        """Insert a customer and return the inserted row"""
        payload = {"name": name, "email": email}
        if phone:
            payload["phone"] = phone
        if city:
            payload["city"] = city

        self._sb.table("customers").insert(payload).execute()

        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_id(self, cust_id: int) -> Optional[Dict]:
        resp = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        resp = self._sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_customer(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        """Update customer and return updated row"""
        self._sb.table("customers").update(fields).eq("cust_id", cust_id).execute()
        resp = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_customer(self, cust_id: int) -> Optional[Dict]:
        """Delete and return deleted row"""
        resp_before = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None

        self._sb.table("customers").delete().eq("cust_id", cust_id).execute()
        return row

    def list_customers(self, limit: int = 100) -> List[Dict]:
        resp = self._sb.table("customers").select("*").order("cust_id", desc=False).limit(limit).execute()
        return resp.data or []
