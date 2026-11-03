import json
import os

from product import Product

INVENTORY_FILE = "inventory.json"


def default_products():
    return [
        Product("P001", "Laptop", 1200.00, 0),
        Product("P002", "Mouse", 25.50, 0),
        Product("P003", "Keyboard", 45.00, 0),
    ]


def load_inventory(inventory, filename=INVENTORY_FILE):
    """Fill the Inventory object with products and history from the JSON file."""
    if not os.path.exists(filename):
        print("No inventory.json found. Starting with default products.")
        for p in default_products():
            inventory.add_product(p)
        return

    try:
        with open(filename, "r") as f:
            data = json.load(f)
        products = []
        for i, item in enumerate(data["products"], start=1):
            # .get() with defaults lets us read the OLD Week 5 file
            # (which only had "name" and "quantity") as well as the new format.
            products.append(Product(
                item.get("product_id", f"P{i:03d}"),
                item["name"],
                item.get("price", 0.0),
                item.get("stock", item.get("quantity", 0)),
            ))
        history = list(data["history"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("⚠️ inventory.json is unreadable. Starting with default products.")
        products, history = default_products(), []

    for p in products:
        inventory.add_product(p)
    for record in history:
        inventory.add_history_record(record)


def save_inventory(inventory, filename=INVENTORY_FILE):
    """Convert Product objects back into dictionaries so JSON can store them."""
    data = {
        "products": [
            {
                "product_id": p.get_product_id(),
                "name": p.get_name(),
                "price": p.get_price(),
                "stock": p.get_stock(),
            }
            for p in inventory.get_products()
        ],
        "history": inventory.get_history(),
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)