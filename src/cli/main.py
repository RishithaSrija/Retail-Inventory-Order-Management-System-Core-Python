import argparse
import json
from src.services.product_service import ProductService
from src.services.order_service import OrderService
from src.services.customer_service import CustomerService
from src.services.payment_services import PaymentService
from src.services.Reporting_Services import ReportService
from src.dao.product_dao import ProductRepository
from src.dao.customer_dao import CustomerRepository
from src.dao.order_dao import OrderRepository
from src.dao.payment_dao import PaymentRepository


class RetailCLI:
    def __init__(self):
        # Services
        self.product_service = ProductService(ProductRepository())
        self.customer_service = CustomerService(CustomerRepository())
        self.order_service = OrderService(OrderRepository(), ProductRepository(), CustomerRepository())
        self.payment_service = PaymentService(PaymentRepository(), OrderRepository())
        self.report_service = ReportService(ProductRepository(), OrderRepository(), CustomerRepository())
        self.parser = self.build_parser()

    # ------------------ PRODUCT ------------------
    def cmd_product_add(self, args):
        try:
            p = self.product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
            print("Created product:")
            print(json.dumps(p, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_product_list(self, args):
        ps = self.product_service.dao.list_products(limit=100)
        print(json.dumps(ps, indent=2, default=str))

    # ------------------ CUSTOMER ------------------
    def cmd_customer_add(self, args):
        try:
            c = self.customer_service.create_customer(args.name, args.email, args.phone, args.city)
            print("Created customer:")
            print(json.dumps(c, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    # ------------------ ORDER ------------------
    def cmd_order_create(self, args):
        items = []
        for item in args.item:
            try:
                pid, qty = item.split(":")
                items.append({"prod_id": int(pid), "quantity": int(qty)})
            except Exception:
                print("Invalid item format:", item)
                return
        try:
            ord = self.order_service.create_order(args.customer, items)
            # Create pending payment automatically
            self.payment_service.create_pending_payment(ord["order_id"], ord["total_amount"])
            print("Order created:")
            print(json.dumps(ord, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_show(self, args):
        try:
            o = self.order_service.get_order_details(args.order)
            print(json.dumps(o, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    def cmd_order_cancel(self, args):
        try:
            self.order_service.cancel_order(args.order)
            self.payment_service.refund_order_payment(args.order)
            print("Order cancelled and payment refunded")
        except Exception as e:
            print("Error:", e)

    # ------------------ PAYMENT ------------------
    def cmd_payment_pay(self, args):
        try:
            payment = self.payment_service.pay_order(args.order, args.method)
            print("Payment processed:")
            print(json.dumps(payment, indent=2, default=str))
        except Exception as e:
            print("Error:", e)

    # ------------------ REPORTS ------------------
    def cmd_report_top_products(self, args):
        top = self.report_service.top_selling_products()
        print("Top selling products:")
        print(json.dumps(top, indent=2, default=str))

    def cmd_report_revenue_last_month(self, args):
        revenue = self.report_service.total_revenue_last_month()
        print(f"Total revenue last month: {revenue}")

    def cmd_report_customer_orders(self, args):
        summary = self.report_service.total_orders_per_customer()
        print("Orders per customer:")
        print(json.dumps(summary, indent=2, default=str))

    def cmd_report_frequent_customers(self, args):
        customers = self.report_service.frequent_customers()
        print("Frequent customers:")
        print(json.dumps(customers, indent=2, default=str))

    # ------------------ CLI BUILDER ------------------
    def build_parser(self):
        parser = argparse.ArgumentParser(prog="retail-cli")
        sub = parser.add_subparsers(dest="cmd")

        # PRODUCT
        p_prod = sub.add_parser("product", help="product commands")
        pprod_sub = p_prod.add_subparsers(dest="action")
        addp = pprod_sub.add_parser("add")
        addp.add_argument("--name", required=True)
        addp.add_argument("--sku", required=True)
        addp.add_argument("--price", type=float, required=True)
        addp.add_argument("--stock", type=int, default=0)
        addp.add_argument("--category", default=None)
        addp.set_defaults(func=self.cmd_product_add)

        listp = pprod_sub.add_parser("list")
        listp.set_defaults(func=self.cmd_product_list)

        # CUSTOMER
        pcust = sub.add_parser("customer")
        pcust_sub = pcust.add_subparsers(dest="action")
        addc = pcust_sub.add_parser("add")
        addc.add_argument("--name", required=True)
        addc.add_argument("--email", required=True)
        addc.add_argument("--phone", required=True)
        addc.add_argument("--city", default=None)
        addc.set_defaults(func=self.cmd_customer_add)

        # ORDER
        porder = sub.add_parser("order")
        porder_sub = porder.add_subparsers(dest="action")
        createo = porder_sub.add_parser("create")
        createo.add_argument("--customer", type=int, required=True)
        createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
        createo.set_defaults(func=self.cmd_order_create)

        showo = porder_sub.add_parser("show")
        showo.add_argument("--order", type=int, required=True)
        showo.set_defaults(func=self.cmd_order_show)

        cano = porder_sub.add_parser("cancel")
        cano.add_argument("--order", type=int, required=True)
        cano.set_defaults(func=self.cmd_order_cancel)

        # PAYMENT
        ppay = sub.add_parser("payment", help="payment commands")
        ppay_sub = ppay.add_subparsers(dest="action")
        pay = ppay_sub.add_parser("pay")
        pay.add_argument("--order", type=int, required=True)
        pay.add_argument("--method", choices=["Cash", "Card", "UPI"], required=True)
        pay.set_defaults(func=self.cmd_payment_pay)

        # REPORTS
        prep = sub.add_parser("report", help="report commands")
        prep_sub = prep.add_subparsers(dest="action")
        top = prep_sub.add_parser("top-products")
        top.set_defaults(func=self.cmd_report_top_products)

        rev = prep_sub.add_parser("revenue-last-month")
        rev.set_defaults(func=self.cmd_report_revenue_last_month)

        cust_orders = prep_sub.add_parser("customer-orders")
        cust_orders.set_defaults(func=self.cmd_report_customer_orders)

        freq_cust = prep_sub.add_parser("frequent-customers")
        freq_cust.set_defaults(func=self.cmd_report_frequent_customers)

        return parser

    def run(self):
        args = self.parser.parse_args()
        if not hasattr(args, "func"):
            self.parser.print_help()
            return
        args.func(args)

def main():
    cli = RetailCLI()
    cli.run()


if __name__ == "__main__":
    main()
