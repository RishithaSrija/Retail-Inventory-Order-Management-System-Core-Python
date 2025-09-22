from typing import Optional, List, Dict

from src.config import get_supabase

 

class CustomerRepository:
    def __init__(self):
        self._sb=get_supabase()

    def create_account(self,name: str, email: str,  phone: int , city: str| None = None) -> Optional[Dict]:
        existing=self._sb._table("customer").select("*").eq('email',email).limit(1).execute()
        if existing.data:
            raise ValueError(f"Email already exists: {email}")
        payload={"name":name,"email":email,"phone":phone}

        if city:
            payload["city"]=city
        
        
        self._sb.table("customers").insert(payload).execute()

        resp=self._sb.table("customers").select("*").eq("email",email).limit(1).execute()
        return resp.data[0] if resp.data else None
    
    def get_customer_by_id(self,cust_id:int)->Optional[Dict]:
        resp=self._sb.table('cutomer').select('*').eq("cust_id",cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None
    def get_customer_by_email(self,email:str)->Optional[Dict]:
        resp=self._sb.table('cutomer').select('*').eq("email",email).limit(1).execute()
        return resp.data[0] if resp.data else None 
    
    def update_customer(self, cust_id: int, phone: str | None = None, city: str | None = None) -> Optional[Dict]:
        fields={}
        if phone:
            fields['phone']=phone

        if city:
            fields['city']=city
        if not fields:
            return self.get_customer_by_id(cust_id)
        self._sb.table("customers").update(fields).eq("cust_id",cust_id).execute()
        resp=self._sb.table("customers").select("*").eq("cust_id",cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None
    

    def delete_customer(self,cust_id:int)->Optional[Dict]:
        orders=self._sb.table('orders').select("order_id").eq("cust_id",cust_id).limit(1).execute()
        if orders.data:
            raise ValueError("Cannot delete customer with existing orders")
        resp_before = self._sb.table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None

        self._sb.table("customers").delete().eq("cust_id", cust_id).execute()
        return row

    def list_customers(self, limit: int = 100) -> List[Dict]:
        resp = self._sb.table("customers").select("*").order("cust_id", desc=False).limit(limit).execute()
        return resp.data or []

    def search_customers(self, email: str | None = None, city: str | None = None) -> List[Dict]:
        """
        Search by email or city.
        """
        q = self._sb.table("customers").select("*")

        if email:
            q = q.eq("email", email)
        if city:
            q = q.eq("city", city)

        resp = q.execute()
        return resp.data or []