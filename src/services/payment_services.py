from src.dao.payment_dao import PaymentRepository
from src.dao.order_dao import OrderRepository

class PaymentService:
    def __init__(self, payment_repo: PaymentRepository, order_repo: OrderRepository):
        self.payment_repo = payment_repo
        self.order_repo = order_repo

    def create_pending_payment(self, order_id: int, amount: float):
        return self.payment_repo.create_payment(order_id, amount)

    def pay_order(self, order_id: int, method: str):
        # mark payment PAID
        payment = self.payment_repo.process_payment(order_id, method)
        # mark order COMPLETED
        self.order_repo.update_order(order_id, {"status": "COMPLETED"})
        return payment

    def refund_order_payment(self, order_id: int):
        # mark payment REFUNDED
        payment = self.payment_repo.refund_payment(order_id)
        # mark order CANCELLED
        self.order_repo.update_order(order_id, {"status": "CANCELLED"})
        return payment
