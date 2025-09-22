# Retail Inventory & Order Management System

A core Python application to manage products, customers, orders, and payments for a retail store. This system uses **Supabase** as the backend database and demonstrates a clean **OOP structure** for modular, maintainable code.

---

## Features

### Products Module
- Add new products with SKU, name, price, stock, and category.
- Restock products.
- View products with low stock alerts.

### Customers Module
- Add new customers with name, email, phone, and city.
- Ensure unique emails.
- Update customer details (phone, city).
- Delete customers (only if no orders exist).
- List all customers and search by email or city.

### Orders Module
- Create new orders for customers with multiple products and quantities.
- Validate customer existence and product stock.
- Automatically update stock when orders are placed.
- Cancel orders (only if status = `PLACED`) and restore stock.
- Fetch full order details including customer info and items.

### Payments Module
- Record pending payments when orders are created.
- Process payments with methods: Cash / Card / UPI.
- Update order status to `COMPLETED` after payment.
- Support refunds for canceled orders.

### Reporting Module
- Show top 5 selling products by quantity.
- View total revenue in the last month.
- Count total orders per customer.
- Identify customers who placed more than 2 orders.

---

## Tech Stack
- **Python 3.11+**
- **Supabase** (PostgreSQL) as backend
- **argparse** for CLI interface
- Modular **OOP design** (Services & Repositories)
- JSON output for CLI commands

---

## Project Structure

