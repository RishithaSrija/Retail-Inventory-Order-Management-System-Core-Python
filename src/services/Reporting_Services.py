from src.dao.product_dao import ProductRepository
from src.dao.order_dao import OrderRepository
from src.dao.customer_dao import CustomerRepository

class ReportService:
    def __init__(self, product_repo: ProductRepository, order_repo: OrderRepository, customer_repo: CustomerRepository):
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.customer_repo = customer_repo

    def top_selling_products(self, limit: int = 5):
        # Aggregate total quantity per product
        resp = self.order_repo._sb.table("order_items").select("prod_id, sum(quantity) as total_qty").group("prod_id").order("total_qty", desc=True).limit(limit).execute()
        return resp.data or []

    def total_revenue_last_month(self):
        from datetime import datetime, timedelta
        now = datetime.now()
        last_month = now - timedelta(days=30)
        resp = self.order_repo._sb.table("orders").select("sum(total_amount)").gte("created_at", last_month.isoformat()).execute()
        return resp.data[0]["sum"] if resp.data else 0

    def total_orders_per_customer(self):
        resp = self.order_repo._sb.table("orders").select("cust_id, count(*) as total_orders").group("cust_id").execute()
        return resp.data or []

    def frequent_customers(self, min_orders: int = 2):
        orders = self.total_orders_per_customer()
        customer_ids = [o["cust_id"] for o in orders if o["total_orders"] > min_orders]
        resp = [self.customer_repo.get_customer_by_id(cid) for cid in customer_ids]
        return resp
