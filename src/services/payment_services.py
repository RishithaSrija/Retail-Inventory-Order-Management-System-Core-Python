# src/services/payment_service.py
from dao.payment_dao import PaymentDAO
from dao.order_dao import OrderDAO
from typing import Dict

class PaymentService:
    def __init__(self, payment_dao: PaymentDAO, order_dao: OrderDAO):
        self.payment_dao = payment_dao
        self.order_dao = order_dao

    def create_pending_payment(self, order_id: int, amount: float) -> Dict:
        """Create a pending payment for a given order"""
        if not order_id:
            raise ValueError("Order ID is required")
        if amount <= 0:
            raise ValueError("Payment amount must be positive")

        # Pending payments have method=None
        return self.payment_dao.create_payment(order_id, amount, method=None, status="PENDING")

    def pay_order(self, order_id: int, method: str) -> Dict:
        """Mark an order as paid using a specific method"""
        if not order_id:
            raise ValueError("Order ID is required")
        if method not in ["Cash", "Card", "UPI"]:
            raise ValueError("Invalid payment method")

        payment = self.payment_dao.get_payment_by_order(order_id)
        if not payment:
            raise LookupError(f"No payment found for order {order_id}")

        return self.payment_dao.update_payment(payment["payment_id"], {"status": "PAID", "method": method})

    def refund_order_payment(self, order_id: int) -> Dict:
        """Refund a payment for a given order"""
        payment = self.payment_dao.get_payment_by_order(order_id)
        if not payment:
            raise LookupError(f"No payment found for order {order_id}")

        return self.payment_dao.update_payment(payment["payment_id"], {"status": "REFUNDED"})
