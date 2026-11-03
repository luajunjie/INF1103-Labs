from product import Product
from inventory import Inventory
from file_handler import load_inventory, save_inventory

LIMIT = 5000
WARNING_RATIO = 0.5
TAX_RATE = 0.10
MAX_FAILED = 3
APPROVED_USERS = ["employee", "manager", "boss"]


# ---------- Input helpers (main program's job: getting user input) ----------
def get_whole_number(prompt):
    """Returns an int >= 0, the string 'quit', or None if invalid."""
    text = input(prompt).strip()
    if text.lower() == "quit":
        return "quit"
    if not text.isdigit():
        print("❌ Error: Please enter a whole number of 0 or more.")
        return None
    return int(text)


def get_price(prompt):
    text = input(prompt).strip()
    try:
        price = float(text)
    except ValueError:
        print("❌ Error: Please enter a valid price.")
        return None
    if price < 0:
        print("❌ Error: Price cannot be negative.")
        return None
    return price


def choose_product(inventory):
    products = inventory.get_products()
    for i, p in enumerate(products, start=1):
        print(f"{i}. {p.get_name()} (in stock: {p.get_stock()})")
    choice = input("Select product number: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(products):
        print("❌ Error: Invalid product number.")
        return None
    return products[int(choice) - 1]


def calculate_tax(amount):
    return amount * TAX_RATE


# ---------- Menu actions ----------
def add_product_menu(inventory):
    name = input("New product name: ").strip()
    if name == "" or "," in name:
        print("❌ Error: Product name cannot be empty or contain commas.")
        return False
    price = get_price("Price: ")
    if price is None:
        return False
    product = Product(inventory.generate_next_id(), name, price, 0)
    if not inventory.add_product(product):
        print(f"❌ Error: {name} already exists.")
        return False
    print(f"✅ {name} added as {product.get_product_id()}.")
    return True


def update_stock_menu(inventory, user):
    """Record a delivery. Returns 'ok', 'failed', 'quit' or 'overstock'."""
    product = choose_product(inventory)
    if product is None:
        return "failed"

    amount = get_whole_number("Enter stock quantity (or type 'quit' to exit): ")
    if amount == "quit":
        return "quit"
    if amount is None:
        return "failed"

    inventory.record_delivery(product, amount, user)
    total = inventory.get_total()
    print(f"\nNew Delivery Added: {product.get_name()}, {amount} units, logged by {user}")
    print(f"✅ Inventory updated. Current total: {total} units")
    print(f"💰 Tax on this delivery: {calculate_tax(amount):.2f}")
    print(f"Limit to overstocking: {LIMIT - total} units")

    if total > LIMIT:
        print(f"⚠️ ALERT: Inventory exceeds {LIMIT} units! Overstock detected. Resetting inventory to 0.")
        inventory.reset_all_stock()
        return "overstock"

    if total >= LIMIT - WARNING_RATIO * LIMIT:
        print(f"⚠️ ALERT: Inventory is close to limit! Units left before reaching {LIMIT}: {LIMIT - total}")
    return "ok"


def generate_report(inventory, failed_entries, deliveries_processed):
    print("\n📊 Final Inventory Report")
    for p in inventory.get_products():
        print(f"  {p.get_name()}: {p.get_stock()} units")
    print(f"Total Inventory: {inventory.get_total()} units")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")
    print(f"Limit to overstocking: {LIMIT - inventory.get_total()} units")


def save_and_exit(inventory, failed_entries, deliveries_processed):
    save_inventory(inventory)
    print("\nInventory successfully saved to inventory.json")
    generate_report(inventory, failed_entries, deliveries_processed)