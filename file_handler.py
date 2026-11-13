import json
import os

from product import Product
from supplier import Supplier
from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

INVENTORY_FILE = "inventory.json"


def default_suppliers() -> list[Supplier]:
    return [
        Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example"),
        Supplier("S002", "SoftWorks Digital", "orders@softworks.example"),
    ]


def default_products(suppliers: dict[str, Supplier]) -> list[Product]:
    hardware = suppliers["S001"]
    software = suppliers["S002"]
    return [
        PhysicalProduct("P001", "Laptop", 1200.00, 0, hardware, weight=2.0),
        PhysicalProduct("P002", "Mouse", 25.50, 0, hardware, weight=0.1),
        PhysicalProduct("P003", "Keyboard", 45.00, 0, hardware, weight=0.8),
        DigitalProduct("P004", "Antivirus Software", 59.90, 0, software, download_size=350.0),
    ]


def supplier_from_dict(item: dict[str, str]) -> Supplier:
    return Supplier(item["supplier_id"], item["name"], item["contact_email"])


def product_from_dict(item: dict[str, str | float], position: int,
                      suppliers: dict[str, Supplier]) -> Product:
    """Use the saved "type" to rebuild the right subclass,
    and the saved "supplier_id" to link it back to its Supplier object."""
    product_id = item.get("product_id", f"P{position:03d}")
    name = item["name"]
    price = item.get("price", 0.0)
    # "quantity" lets us still read the old Week 5 file format
    stock = int(item.get("stock", item.get("quantity", 0)))
    product_type = item.get("type", "physical")  # older files had no type
    # Older files had no supplier, so fall back to the first supplier
    supplier = suppliers.get(item.get("supplier_id", ""), next(iter(suppliers.values())))

    if product_type == "digital":
        return DigitalProduct(product_id, name, price, stock, supplier, item.get("download_size", 0.0))
    if product_type == "physical":
        return PhysicalProduct(product_id, name, price, stock, supplier, item.get("weight", 0.0))
    raise ValueError(f"Unknown product type: {product_type}")


def load_inventory(inventory: Inventory, filename: str = INVENTORY_FILE) -> list[Supplier]:
    """Fill the Inventory with products and history. Returns the list of suppliers."""
    if not os.path.exists(filename):
        print("No inventory.json found. Starting with default products.")
        suppliers = default_suppliers()
        lookup = {s.get_supplier_id(): s for s in suppliers}
        for p in default_products(lookup):
            inventory.add_product(p)
        return suppliers

    try:
        with open(filename, "r") as f:
            data = json.load(f)
        # Suppliers are loaded FIRST, because products need to link to them
        suppliers = [supplier_from_dict(s) for s in data.get("suppliers", [])] or default_suppliers()
        lookup = {s.get_supplier_id(): s for s in suppliers}
        products = [product_from_dict(item, i, lookup) for i, item in enumerate(data["products"], start=1)]
        history = list(data["history"])
    except (json.JSONDecodeError, KeyError, TypeError, ValueError):
        print("⚠️ inventory.json is unreadable. Starting with default products.")
        suppliers = default_suppliers()
        products = default_products({s.get_supplier_id(): s for s in suppliers})
        history = []

    for p in products:
        inventory.add_product(p)
    for record in history:
        inventory.add_history_record(record)
    return suppliers


def save_inventory(inventory: Inventory, suppliers: list[Supplier],
                   filename: str = INVENTORY_FILE) -> None:
    """Each supplier and product turns itself into a dictionary."""
    data = {
        "suppliers": [s.to_dict() for s in suppliers],
        "products": [p.to_dict() for p in inventory.get_products()],
        "history": inventory.get_history(),
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)