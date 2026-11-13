from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from file_handler import load_inventory, save_inventory

LIMIT: int = 5000
WARNING_RATIO: float = 0.5
TAX_RATE: float = 0.10
MAX_FAILED: int = 3
APPROVED_USERS: list[str] = ["employee", "manager", "boss"]


def get_whole_number(prompt: str) -> int | str | None:
    text = input(prompt).strip()
    if text.lower() == "quit":
        return "quit"
    if not text.isdigit():
        print(" Error: Please enter a whole number of 0 or more.")
        return None
    return int(text)


def get_positive_number(prompt: str, label: str) -> float | None:
    text = input(prompt).strip()
    try:
        value = float(text)
    except ValueError:
        print(f" Error: Please enter a valid {label}.")
        return None
    if value < 0:
        print(f" Error: {label.capitalize()} cannot be negative.")
        return None
    return value


def choose_product(inventory: Inventory) -> Product | None:
    products = inventory.get_products()
    for i, p in enumerate(products, start=1):
        print(f"{i}. {p.get_name()} (in stock: {p.get_stock()})")
    choice = input("Select product number: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(products):
        print(" Error: Invalid product number.")
        return None
    return products[int(choice) - 1]

def choose_supplier(suppliers: list[Supplier]) -> Supplier | None:
    for i, s in enumerate(suppliers, start=1):
        print(f"{i}. {s.get_name()} ({s.get_contact_email()})")
    choice = input("Select supplier number: ").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(suppliers):
        print("❌ Error: Invalid supplier number.")
        return None
    return suppliers[int(choice) - 1]


def calculate_tax(amount: int) -> float:
    return amount * TAX_RATE

def add_supplier_menu(suppliers: list[Supplier]) -> bool:
    name = input("Supplier name: ").strip()
    if name == "":
        print("Supplier name cannot be empty.")
        return False
    email = input("Contact email: ").strip()
    if "@" not in email or "." not in email:
        print("Please enter a valid email address.")
        return False
    supplier = Supplier(f"S{len(suppliers) + 1:03d}", name, email)
    suppliers.append(supplier)
    print(f"Supplier {name} added as {supplier.get_supplier_id()}.")
    return True


# ---------- Menu actions ----------
def add_product_menu(inventory: Inventory, suppliers: list[Supplier]) -> bool:
    supplier = choose_supplier(suppliers)
    name = input("New product name: ").strip()
    if name == "" or "," in name:
        print(" Error: Product name cannot be empty or contain commas.")
        return False
    price = get_positive_number("Price: ", "price")
    if price is None:
        return False
    
    if supplier is None:
          return False

    product_type = input("Product type - 1. Physical  2. Digital: ").strip()
    product_id = inventory.generate_next_id()
    if product_type == "1":
        weight = get_positive_number("Weight (kg): ", "weight")
        if weight is None:
            return False
        product = PhysicalProduct(product_id, name, price, 0, supplier, weight)
    elif product_type == "2":
        size = get_positive_number("Download size (MB): ", "download size")
        if size is None:
            return False
        product = DigitalProduct(product_id, name, price, 0, supplier, size)
    else:
        print(" Error: Please choose 1 or 2.")
        return False
    if not inventory.add_product(product):
        print(f" Error: {name} already exists.")
        return False
    print(f" {name} added as {product.get_product_id()}.")
    return True

def remove_product_menu(inventory: Inventory) -> bool:
    product = choose_product(inventory)
    if product is None:
        return False
    removed = inventory.remove_product(product.get_product_id())
    print(f"✅ {removed.get_name()} removed from the inventory.")
    return True


def create_order_menu(inventory: Inventory, orders: list[Order]) -> bool:
    order = Order(f"O{len(orders) + 1:03d}")
    while True:
        product = choose_product(inventory)
        if product is None:
            return False
        quantity = get_whole_number("Quantity: ")
        if not isinstance(quantity, int) or quantity == 0:
            print("Quantity must be a whole number above 0.")
            return False
        order.add_order_line(product, quantity)  # the Order creates the OrderLine itself
        if input("Add another product? (y/n): ").strip().lower() != "y":
            break
    orders.append(order)
    order.display_information()
    return True


def update_stock_menu(inventory: Inventory, user: str) -> str:
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
    print(f" Inventory updated. Current total: {total} units")
    print(f" Tax on this delivery: {calculate_tax(amount):.2f}")
    print(f"Limit to overstocking: {LIMIT - total} units")

    if total > LIMIT:
        print(f" ALERT: Inventory exceeds {LIMIT} units! Overstock detected. Resetting inventory to 0.")
        inventory.reset_all_stock()
        return "overstock"

    if total >= LIMIT - WARNING_RATIO * LIMIT:
        print(f" ALERT: Inventory is close to limit! Units left before reaching {LIMIT}: {LIMIT - total}")
    return "ok"


def generate_report(inventory: Inventory, failed_entries: int, deliveries_processed: int) -> None:
    print("\n Final Inventory Report")
    for p in inventory.get_products():
        print(f"  {p.get_name()}: {p.get_stock()} units")
    print(f"Total Inventory: {inventory.get_total()} units")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_entries}")
    print(f"Limit to overstocking: {LIMIT - inventory.get_total()} units")


def save_and_exit(inventory: Inventory, suppliers: list[Supplier],
                  failed_entries: int, deliveries_processed: int) -> None:
    save_inventory(inventory, suppliers)
    print("\nInventory successfully saved to inventory.json")
    generate_report(inventory, failed_entries, deliveries_processed)


def main() -> None:
    inventory = Inventory()
    suppliers: list[Supplier] = load_inventory(inventory)
    orders: list[Order] = []  # kept for this session only

    user = input("Enter username for authentication purposes: ").strip()
    if user not in APPROVED_USERS:
        print("Access unauthorized. Ending programme.")
        return
    print(f" Access successful! Logged in as: {user}")
    inventory.display_all()
    inventory.display_history()

    failed_entries = 0
    deliveries_processed = 0

    while True:
        if failed_entries >= MAX_FAILED:
            print(f" You have entered errors {MAX_FAILED} times. Exiting programme.")
            save_and_exit(inventory, suppliers, failed_entries, deliveries_processed)
            break

        print("\n1. Display all  2. Add product  3. Update stock (record delivery)"
              "  4. Search product  5. Delivery history  6. Save  7. Exit"
              "\n8. Add supplier  9. Remove product  10. Create order")
        choice = input("Choose an option: ").strip().lower()

        if choice in ("7", "quit", "exit"):
            save_and_exit(inventory, suppliers, failed_entries, deliveries_processed)
            break

        elif choice == "1":
            inventory.display_all()

        elif choice == "2":
            if not add_product_menu(inventory, suppliers):
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
                save_and_exit(inventory, suppliers, failed_entries, deliveries_processed)
                break
            elif result == "overstock":
                save_inventory(inventory, suppliers)
                break

        elif choice == "4":
            name = input("Product name to search: ")
            found = inventory.search_product(name, partial=True)
            if found:
                print(" Found:", end=" ")
                found.display_information()
                print(f"    Fulfilment: {found.get_fulfilment_info()}")
            else:
                print(" Product not found.")
           
        elif choice == "5":
            inventory.display_history()

        elif choice == "6":
            save_inventory(inventory, suppliers)
            print(" Inventory saved to inventory.json")

        elif choice in ("8", "9", "10"):
            if choice == "8":
                ok = add_supplier_menu(suppliers)
            elif choice == "9":
                ok = remove_product_menu(inventory)
            else:
                ok = create_order_menu(inventory, orders)
            if not ok:
                failed_entries += 1
                print(f"Times of Error: {failed_entries}")    

        else:
            print(" Error: Invalid option.")
            failed_entries += 1
            print(f"Times of Error: {failed_entries}")



if __name__ == "__main__":
    main()