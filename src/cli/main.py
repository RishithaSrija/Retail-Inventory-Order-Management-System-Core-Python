# python -m src.cli.main
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from services.product_service import ProductService
from services.customer_service import CustomerService
from services.order_service import OrderService
from services.payment_services import PaymentService
from services.reporting_services import ReportingService
from dao.product_dao import ProductDAO
from dao.customer_dao import CustomerDAO
from dao.order_dao import OrderDAO
from dao.payment_dao import PaymentDAO
from dao.order_item_dao import OrderItemDAO

class RetailCLI:
    def __init__(self):
        # Initialize DAOs
        self.product_dao = ProductDAO()
        self.customer_dao = CustomerDAO()
        self.order_dao = OrderDAO()
        self.payment_dao = PaymentDAO()
        self.order_item_dao = OrderItemDAO() 
        # Initialize services
        self.product_service = ProductService(self.product_dao)
        self.customer_service = CustomerService(self.customer_dao)
        self.order_service = OrderService(self.order_dao, self.product_dao, self.customer_dao)
        self.payment_service = PaymentService(self.payment_dao, self.order_dao)
        self.reporting_service = ReportingService(self.product_dao, self.order_dao, self.customer_dao,self.order_item_dao)

    # ------------------ PRODUCT ------------------
    def product_menu(self):
        print("\n--- Product Menu ---")
        print("1. Add Product")
        print("2. List Products")
        print("0. Back")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            try:
                name = input("Name: ")
                sku = input("SKU: ")
                price = float(input("Price: "))
                stock = int(input("Stock: "))
                category = input("Category (optional): ") or None
                product = self.product_service.add_product(name, sku, price, stock, category)
                print("Created product:")
                print(json.dumps(product, indent=2, default=str))
            except Exception as e:
                print("Error:", e)
        elif choice == "2":
            products = self.product_service.list_products(limit=100)
            print(json.dumps(products, indent=2, default=str))
        elif choice == "0":
            return
        else:
            print("Invalid choice")

    # ------------------ CUSTOMER ------------------
    def customer_menu(self):
        while True:
            print("\n--- Customer Menu ---")
            print("1. Add Customer")
            print("2. List Customers")
            print("3. Update Customer")
            print("4. Delete Customer")
            print("0. Back")
            choice = input("Enter choice: ").strip()

            if choice == "1":
                try:
                    name = input("Name: ")
                    email = input("Email: ")
                    phone = input("Phone: ") or None
                    city = input("City (optional): ") or None
                    customer = self.customer_service.add_customer(name, email, phone, city)
                    print("Created customer:")
                    print(json.dumps(customer, indent=2, default=str))
                except Exception as e:
                    print("Error:", e)

            elif choice == "2":
                customers = self.customer_service.list_customers()
                print(json.dumps(customers, indent=2, default=str))

            elif choice == "3":
                try:
                    cust_id = int(input("Customer ID to update: "))
                    fields = {}
                    name = input("Name (leave blank to skip): ")
                    if name: fields["name"] = name
                    email = input("Email (leave blank to skip): ")
                    if email: fields["email"] = email
                    phone = input("Phone (leave blank to skip): ")
                    if phone: fields["phone"] = phone
                    city = input("City (leave blank to skip): ")
                    if city: fields["city"] = city
                    updated = self.customer_service.update_customer(cust_id, fields)
                    print("Updated customer:", updated)
                except Exception as e:
                    print("Error:", e)

            elif choice == "4":
                try:
                    cust_id = int(input("Customer ID to delete: "))
                    self.customer_service.delete_customer(cust_id)
                    print(f"Customer {cust_id} deleted successfully")
                except Exception as e:
                    print("Error:", e)

            elif choice == "0":
                break
            else:
                print("Invalid choice!")

    # ------------------ ORDER ------------------
    def order_menu(self):
     while True:
        print("\n--- Order Menu ---")
        print("1. Create Order")
        print("2. Show Order Details")
        print("3. Cancel Order")
        print("4. List Orders")
        print("0. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            try:
                cust_id = int(input("Customer ID: "))
                items_input = input("Enter items (prod_id:qty, separated by commas): ")
                items = [{"prod_id": int(pid), "quantity": int(qty)} 
                         for pid, qty in (item.strip().split(":") for item in items_input.split(","))]
                order = self.order_service.create_order(cust_id, items)
                self.payment_service.create_pending_payment(order["order_id"], order["total_amount"])
                print("Order created:")
                print(json.dumps(order, indent=2, default=str))
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            try:
                order_id = int(input("Order ID: "))
                order = self.order_service.get_order_details(order_id)
                print(json.dumps(order, indent=2, default=str))
            except Exception as e:
                print("Error:", e)

        elif choice == "3":
            try:
                order_id = int(input("Order ID to cancel: "))
                self.order_service.cancel_order(order_id)
                self.payment_service.refund_order_payment(order_id)
                print(f"Order {order_id} cancelled and payment refunded")
            except Exception as e:
                print("Error:", e)

        elif choice == "4":
            try:
                cust_id_input = input("Customer ID (optional, leave blank for all): ").strip()
                cust_id = int(cust_id_input) if cust_id_input else None
                orders = self.order_service.list_orders(cust_id)
                print(json.dumps(orders, indent=2, default=str))
            except Exception as e:
                print("Error:", e)

        elif choice == "0":
            break
        else:
            print("Invalid choice!")


    # ------------------ PAYMENT ------------------
    def payment_menu(self):
        print("\n--- Payment Menu ---")
        print("1. Pay Order")
        print("0. Back")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            try:
                order_id = int(input("Order ID: "))
                method = input("Payment Method (Cash/Card/UPI): ")
                payment = self.payment_service.pay_order(order_id, method)
                print("Payment processed:")
                print(json.dumps(payment, indent=2, default=str))
            except Exception as e:
                print("Error:", e)
        elif choice == "0":
            return
        else:
            print("Invalid choice")

    # ------------------ REPORT ------------------
    def report_menu(self):
        print("\n--- Reports Menu ---")
        print("1. Top Selling Products")
        print("2. Total Revenue Last Month")
        print("3. Orders per Customer")
        print("4. Frequent Customers")
        print("0. Back")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            top = self.reporting_service.top_selling_products()
            print("Top selling products:")
            print(json.dumps(top, indent=2, default=str))
        elif choice == "2":
            revenue = self.reporting_service.total_revenue_last_month()
            print(f"Total revenue last month: {revenue}")
        elif choice == "3":
            summary = self.reporting_service.total_orders_per_customer()
            print("Orders per customer:")
            print(json.dumps(summary, indent=2, default=str))
        elif choice == "4":
            customers = self.reporting_service.frequent_customers()
            print("Frequent customers:")
            print(json.dumps(customers, indent=2, default=str))
        elif choice == "0":
            return
        else:
            print("Invalid choice")

    # ------------------ MAIN MENU ------------------
    def main_menu(self):
        while True:
            print("\n=== Retail Management CLI ===")
            print("1. Products")
            print("2. Customers")
            print("3. Orders")
            print("4. Payments")
            print("5. Reports")
            print("0. Exit")
            choice = input("Enter choice: ").strip()
            if choice == "1":
                self.product_menu()
            elif choice == "2":
                self.customer_menu()
            elif choice == "3":
                self.order_menu()
            elif choice == "4":
                self.payment_menu()
            elif choice == "5":
                self.report_menu()
            elif choice == "0":
                print("Exiting...")
                break
            else:
                print("Invalid choice, try again.")


def main():
    cli = RetailCLI()
    cli.main_menu()


if __name__ == "__main__":
    main()
