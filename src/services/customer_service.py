
from typing import List, Dict

import src.dao.customer_dao as customer_dao

 

class CustomerError(Exception):

    def __init__(self,message:str):
        super().__init__(message)

class CustomerService:
    def __init__(self,dao=customer_dao):
        self.dao=dao

    def add_customer(self,name:str,email:str,phone:str| None = None, address: str | None = None)-> Dict:
        """Validate and insert a new customer"""
        if not name.strip():
            raise CustomerError("Customer name cannot be empty")
        
        if not email or "@" not in email:
            raise CustomerError("Invalid email address")
        
        existing=self.dao.get_customer_by_email(email)
        if existing:
            raise CustomerError(f"Customer with email {email} already exists")
        return self.dao.create_customer(name,email,phone,address)
    
    def update_customer(self,cust_id: int,fields:Dict)->Dict:
        if not fields:
            raise CustomerError("No fields provided for updation")
        existing=self.dao.get_customer_by_id(cust_id)
        if not existing:
            raise CustomerError("Customer not found")
        return self.dao.update_customer(cust_id,fields)
    
    def delete_customer(self,cust_id: int)-> Dict:
        existing=self.dao.get_customer_by_id(cust_id)
        if not existing:
            raise CustomerError("Customer not found")
        return self.dao.delete_customer(cust_id)
    
    def list_customers(self,limit: int =100)->List[Dict]:

        return self.dao.list_customers(limit)
        

