import json
import os

from physical_product import PhysicalProduct
from digital_product import DigitalProduct

INVENTORY_FILE = "inventory.json"


def default_products():
    return [
        PhysicalProduct("P001", "Laptop", 1200.00, 0, weight=2.0),
        PhysicalProduct("P002", "Mouse", 25.50, 0, weight=0.1),
        PhysicalProduct("P003", "Keyboard", 45.00, 0, weight=0.8),
        DigitalProduct("P004", "Antivirus Software", 59.90, 0, download_size=350.0),
    ]


def product_from_dict(item, position):
    product_id = item.get("product_id", f"P{position:03d}")
    name = item["name"]
    price = item.get("price", 0.0)
    # "quantity" lets us still read the old Week 5 file format
    stock = item.get("stock", item.get("quantity", 0))
    product_type = item.get("type", "physical")  # older files had no type

    if product_type == "digital":
        return DigitalProduct(product_id, name, price, stock, item.get("download_size", 0.0))
    if product_type == "physical":
        return PhysicalProduct(product_id, name, price, stock, item.get("weight", 0.0))
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory(inventory, filename=INVENTORY_FILE):
    if not os.path.exists(filename):
        print("No inventory.json found. Starting with default products.")
        for p in default_products():
            inventory.add_product(p)
        return

    try:
        with open(filename, "r") as f:
            data = json.load(f)
        products = [product_from_dict(item, i) for i, item in enumerate(data["products"], start=1)]
        history = list(data["history"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("⚠️ inventory.json is unreadable. Starting with default products.")
        products, history = default_products(), []

    for p in products:
        inventory.add_product(p)
    for record in history:
        inventory.add_history_record(record)


def save_inventory(inventory, filename=INVENTORY_FILE):
    data = {
        "products": [p.to_dict() for p in inventory.get_products()],
        "history": inventory.get_history(),
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)