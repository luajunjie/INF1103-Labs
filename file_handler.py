import csv
import json
import os

from product import Product
from supplier import Supplier
from inventory import Inventory
from product_factory import ProductFactory

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
        ProductFactory.create("physical", "P001", "Laptop", 1200.00, 0, hardware, 2.0),
        ProductFactory.create("physical", "P002", "Mouse", 25.50, 0, hardware, 0.1),
        ProductFactory.create("physical", "P003", "Keyboard", 45.00, 0, hardware, 0.8),
        ProductFactory.create("digital", "P004", "Antivirus Software", 59.90, 0, software, 350.0),
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
    # The extra detail is saved as "weight" or "download_size" depending on the type
    extra = item.get("weight", item.get("download_size", 0.0))

    # The factory decides which subclass to build (and rejects unknown types)
    return ProductFactory.create(product_type, product_id, name, price, stock, supplier, extra)


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


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Read products from a CSV file, build each one through the ProductFactory,
    and add it to the inventory. Bad rows are reported and skipped."""
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            loaded = 0
            for line_number, row in enumerate(reader, start=2):  # line 1 is the header
                try:
                    product_type, product_id, name, price, stock_quantity = row
                    product = ProductFactory.create(product_type, product_id, name,
                                                    float(price), int(stock_quantity), supplier)
                except ValueError as error:
                    print(f"Skipping row {line_number} {row}: {error}")
                    continue  # one bad row should not stop the rest loading
                if inventory.add_product(product):
                    loaded += 1
                else:
                    print(f"Skipping row {line_number}: {name} ({product_id}) already exists.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
