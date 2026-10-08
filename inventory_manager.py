INVENTORY_FILE = "inventory.txt"

def default_products():
    return [
        {"name": "Laptop", "quantity": 0},
        {"name": "Mouse", "quantity": 0},
        {"name": "Keyboard", "quantity": 0},
    ]


def get_total(products):
    total = 0
    for p in products:
        total += p["quantity"]
    return total


def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as f:
            lines = f.read().splitlines()
        split = lines.index("#history")   # ValueError if missing
        products = []
        for line in lines[:split]:
            name, qty = line.split(",")
            products.append({"name": name, "quantity": int(qty)})
        history = []
        for line in lines[split + 1:]:
            name, amt = line.split(",")
            history.append({"product": name, "amount": int(amt)})
        if len(products) < 3:
            raise ValueError
        return products, history
    except FileNotFoundError:
        return default_products(), []
    except (ValueError, IndexError):
        print("⚠️ Inventory file is unreadable. Starting with an empty inventory.")
        return default_products(), []


def save_inventory(products, history):
    with open(INVENTORY_FILE, "w") as f:
        for p in products:
            f.write(f"{p['name']},{p['quantity']}\n")
        f.write("#history\n")
        for h in history:
            f.write(f"{h['product']},{h['amount']}\n")

def get_valid_input():
    
    user_input = input("Enter stock quantity (or type 'quit' to exit): ")

    if user_input.lower() == "quit":
        return "quit"

    if not user_input.isdigit():
        print("❌ Error: Please enter a valid integer.")
        return None

    stock = int(user_input)
    if stock < 0:
        print("❌ Error: Negative values are not allowed.")
        return None

    return stock


def process_delivery(current_total, new_value):
   
    return current_total + new_value


def choose_product(products):
    for i, p in enumerate(products, start=1):
        print(f"{i}. {p['name']} (in stock: {p['quantity']})")
    choice = input("Select product number: ")
    if not choice.isdigit() or not 1 <= int(choice) <= len(products):
        print("❌ Error: Invalid product number.")
        return None
    return products[int(choice) - 1]

def search_product(products, name):
    for p in products:
        if p["name"].lower() == name.strip().lower():
            return p
    return None


def add_product(products, name, quantity=0):
    name = name.strip()
    if name == "" or "," in name:
        print("❌ Error: Product name cannot be empty or contain commas.")
        return False
    if search_product(products, name) is not None:
        print(f"❌ Error: {name} already exists.")
        return False
    products.append({"name": name, "quantity": quantity})
    return True


def update_stock(products, name, amount):
    product = search_product(products, name)
    if product is None:
        return False
    product["quantity"] = process_delivery(product["quantity"], amount)
    return True


def display_all(products):
    print("\n📦 All Products:")
    for i, p in enumerate(products, start=1):
        print(f"{i}. {p['name']}: {p['quantity']} units")
    print(f"Total: {get_total(products)} units")


def calculate_tax(amount):
    
    return amount * 0.10


def generate_report(products, failed_attempts, deliveries_processed, history):
    print("\n📊 Final Inventory Report")
    for p in products:
        print(f"  {p['name']}: {p['quantity']} units")
    print(f"Total Inventory: {get_total(products)} units")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History: {history}")

def display_inventory(products, history):
    display_all(products)
    for i, h in enumerate(history, start=1):
        print(f"{i}, Delivery, {h['product']}, {h['amount']}")


def main():
    products, transaction_history = load_inventory()
    inventory = get_total(products)
    limit = 5000
    warning = 0.5
    amount = warning * limit
    approved_username = ['employee', 'manager', 'boss']
    failed_entries = 0
    deliveries_processed = 0
    
    

    # Authentication
    user_auth = input("Enter username for authentication purposes: ")
    if user_auth in approved_username:
        print(f"✅ Access successful! Logged in as: {user_auth}")
        print(f"Loaded inventory: {inventory} units")
        display_inventory(products, transaction_history)
    else:
        print("Access unauthorized. Ending programme.")
        exit()

    while True:
        # Stop if too many failed attempts
        if failed_entries == 3:
            print("❌ You have entered errors 3 times. Exiting programme.")
            break

        user_input = get_valid_input()

        if user_input == "quit":
            save_inventory(products, transaction_history)
            print("\nInventory successfully saved to inventory.txt")
            generate_report(products, failed_entries, deliveries_processed, transaction_history)
            print(f"Limit to overstocking: {limit - inventory} units")
            break

        if user_input is None:
            failed_entries += 1
            print(f"Times of Error: {failed_entries}")
            continue

        product = choose_product(products)
        if product is None:
            failed_entries += 1
            print(f"Times of Error: {failed_entries}")
            continue

        # Process valid delivery
        product["quantity"] = process_delivery(product["quantity"], user_input)
        deliveries_processed += 1
        inventory = get_total(products)
        transaction_history.append({"product": product["name"], "amount": user_input})
        print(f"\nNew Delivery Added:\n{len(transaction_history)}, Delivery, {product['name']}, {user_input}")
        tax = calculate_tax(user_input)
        failed_entries = 0 #Reset after a good entry

        print(f"✅ Inventory updated. Current total: {inventory} units")
        print(f"💰 Tax on this delivery: {tax:.2f}")
        print(f"Limit to overstocking: {limit - inventory} units")

        # Check for overstock
        if inventory > limit:
            print(f"⚠️ ALERT: Inventory exceeds {limit} units! Overstock detected. Resetting inventory to 0.")
            for p in products:
                p["quantity"] = 0
            inventory = 0
            save_inventory(products, transaction_history)
            break

        # Warning when close to limit
        if inventory >= limit - amount:
            print(f"⚠️ ALERT: Inventory is close to limit! Units left before reaching {limit}: {limit - inventory}")


if __name__ == "__main__":
    main()
