from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from can_be_shipped import CanBeShipped
from inventory import Inventory
from file_handler import load_inventory, save_inventory

LIMIT = 5000
WARNING_RATIO = 0.5
TAX_RATE = 0.10
MAX_FAILED = 3
APPROVED_USERS = ["employee", "manager", "boss"]


def get_whole_number(prompt):
    text = input(prompt).strip()
    if text.lower() == "quit":
        return "quit"
    if not text.isdigit():
        print("❌ Error: Please enter a whole number of 0 or more.")
        return None
    return int(text)


def get_positive_number(prompt, label):
    text = input(prompt).strip()
    try:
        value = float(text)
    except ValueError:
        print(f"❌ Error: Please enter a valid {label}.")
        return None
    if value < 0:
        print(f"❌ Error: {label.capitalize()} cannot be negative.")
        return None
    return value


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
    price = get_positive_number("Price: ", "price")
    if price is None:
        return False

    product_type = input("Product type - 1. Physical  2. Digital: ").strip()
    product_id = inventory.generate_next_id()
    if product_type == "1":
        weight = get_positive_number("Weight (kg): ", "weight")
        if weight is None:
            return False
        product = PhysicalProduct(product_id, name, price, 0, weight)
    elif product_type == "2":
        size = get_positive_number("Download size (MB): ", "download size")
        if size is None:
            return False
        product = DigitalProduct(product_id, name, price, 0, size)
    else:
        print("❌ Error: Please choose 1 or 2.")
        return False
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


def main():
    inventory = Inventory()
    load_inventory(inventory)

    user = input("Enter username for authentication purposes: ").strip()
    if user not in APPROVED_USERS:
        print("Access unauthorized. Ending programme.")
        return
    print(f"✅ Access successful! Logged in as: {user}")
    inventory.display_all()
    inventory.display_history()

    failed_entries = 0
    deliveries_processed = 0

    while True:
        if failed_entries >= MAX_FAILED:
            print(f"❌ You have entered errors {MAX_FAILED} times. Exiting programme.")
            save_and_exit(inventory, failed_entries, deliveries_processed)
            break

        print("\n1. Display all  2. Add product  3. Update stock (record delivery)"
              "  4. Search product  5. Delivery history  6. Save  7. Exit")
        choice = input("Choose an option: ").strip().lower()

        if choice in ("7", "quit", "exit"):
            save_and_exit(inventory, failed_entries, deliveries_processed)
            break

        elif choice == "1":
            inventory.display_all()

        elif choice == "2":
            if not add_product_menu(inventory):
                failed_entries += 1
                print(f"Times of Error: {failed_entries}")

        elif choice == "3":
            result = update_stock_menu(inventory, user)
            if result == "ok":
                deliveries_processed += 1
                failed_entries = 0  # reset after a good entry
            elif result == "failed":
                failed_entries += 1
                print(f"Times of Error: {failed_entries}")
            elif result == "quit":
                save_and_exit(inventory, failed_entries, deliveries_processed)
                break
            elif result == "overstock":
                save_inventory(inventory)
                break

        elif choice == "4":
            name = input("Product name to search: ")
            found = inventory.search_product(name, partial=True)
            if found:
                print("🔍 Found:", end=" ")
                found.display_information()
                print(f"    Fulfilment: {found.get_fulfilment_info()}")
                if isinstance(found, CanBeShipped):
                    print(f"    Shipping cost: ${found.calculate_shipping_cost():.2f}")
            else:
                print("❌ Product not found.")
           


        elif choice == "5":
            inventory.display_history()

        elif choice == "6":
            save_inventory(inventory)
            print("💾 Inventory saved to inventory.json")

        else:
            print("❌ Error: Invalid option.")
            failed_entries += 1
            print(f"Times of Error: {failed_entries}")


if __name__ == "__main__":
    main()