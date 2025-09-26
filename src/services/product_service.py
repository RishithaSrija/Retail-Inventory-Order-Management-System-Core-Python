from typing import Optional, Dict, List
from dao.product_dao import ProductDAO


class ProductError(Exception):
    """Custom exception for product-related errors."""
    pass


class ProductService:
    def __init__(self, dao: ProductDAO):
        self.dao = dao

    def add_product(
        self,
        name: str,
        sku: str,
        price: float,
        stock: int = 0,
        category: Optional[str] = None,
    ) -> Dict:
        """
        Validate and add a new product.
        Raises ProductError on validation failure.
        """
        if price <= 0:
            raise ProductError("Price must be greater than 0")

        existing = self.dao.get_product_by_sku(sku)
        if existing:
            raise ProductError(f"SKU already exists: {sku}")

        return self.dao.create_product(name, sku, price, stock, category)

    def restock_product(self, prod_id: int, delta: int) -> Dict:
        """
        Increase stock of a product.
        Raises ProductError if delta <= 0 or product not found.
        """
        if delta <= 0:
            raise ProductError("Restock quantity must be positive")

        product = self.dao.get_product_by_id(prod_id)
        if not product:
            raise ProductError(f"Product not found: {prod_id}")

        new_stock = (product.get("stock") or 0) + delta
        return self.dao.update_product(prod_id, {"stock": new_stock})

    def get_low_stock(self, threshold: int = 5) -> List[Dict]:
        """
        Return a list of products with stock <= threshold.
        """
        all_products = self.dao.list_products(limit=1000)
        return [p for p in all_products if (p.get("stock") or 0) <= threshold]

    def list_products(self, limit: int = 100, category: Optional[str] = None) -> List[Dict]:
        """
        List products optionally filtered by category.
        """
        return self.dao.list_products(limit=limit, category=category)

    def update_product(self, prod_id: int, fields: Dict) -> Dict:
        """
        Update product details. Raises ProductError if product not found.
        """
        product = self.dao.get_product_by_id(prod_id)
        if not product:
            raise ProductError(f"Product not found: {prod_id}")

        return self.dao.update_product(prod_id, fields)

    def delete_product(self, prod_id: int) -> Dict:
        """
        Delete a product. Raises ProductError if product not found.
        """
        product = self.dao.get_product_by_id(prod_id)
        if not product:
            raise ProductError(f"Product not found: {prod_id}")

        return self.dao.delete_product(prod_id)
