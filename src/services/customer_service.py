# src/services/customer_service.py

from typing import Optional, Dict, List
from src.dao.customer_dao import CustomerRepository

class CustomerError(Exception):
    """Custom exception for customer-related errors."""
    pass

class CustomerService:
    def __init__(self, repository: CustomerRepository):
        self.repo = repository

    def create_customer(self, name: str, email: str, phone: str, city: str | None = None) -> Dict:
        """
        Create a new customer after validating unique email.
        """
        existing = self.repo.get_customer_by_email(email)
        if existing:
            raise CustomerError(f"Email already exists: {email}")
        return self.repo.create_account(name, email, phone, city)

    def get_customer(self, cust_id: int) -> Optional[Dict]:
        return self.repo.get_customer_by_id(cust_id)

    def update_customer(self, cust_id: int, phone: str | None = None, city: str | None = None) -> Dict:
        """
        Update customer's phone or city. Raises error if nothing to update.
        """
        if not phone and not city:
            raise CustomerError("Nothing to update: provide phone and/or city")
        updated = self.repo.update_Customer(cust_id, phone, city)
        if not updated:
            raise CustomerError(f"Customer with ID {cust_id} not found")
        return updated

    def delete_customer(self, cust_id: int) -> Dict:
        """
        Delete customer only if no orders exist. Raises error otherwise.
        """
        try:
            return self.repo.delete_customer(cust_id)
        except ValueError as e:
            raise CustomerError(str(e))

    def list_customers(self, limit: int = 100) -> List[Dict]:
        return self.repo.list_customers(limit)

    def search_customers(self, email: str | None = None, city: str | None = None) -> List[Dict]:
        """
        Search customers by email or city.
        """
        return self.repo.search_customers(email, city)
