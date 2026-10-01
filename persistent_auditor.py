INVENTORY_FILE = "inventory.txt"

def load_inventory():
    try:
        with open(INVENTORY_FILE, "r") as f:
            lines = f.read().splitlines()
        total = int(lines[0])
        if len(lines) > 1 and lines[1].strip():
            history = [int(x) for x in lines[1].split(",")]
        else:
            history = []
        return total, history
    except FileNotFoundError:
        return 0, []  # no file yet: start empty, no error
    except (ValueError, IndexError):
        print("⚠️ Inventory file is unreadable. Starting with an empty inventory.")
        return 0, []


def save_inventory(total, history):
    with open(INVENTORY_FILE, "w") as f:
        f.write(f"{total}\n")
        f.write(",".join(str(x) for x in history))


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


def calculate_tax(amount):
    
    return amount * 0.10


def generate_report(total_units, failed_attempts, deliveries_processed, history):
    print("\n📊 Final Inventory Report")
    print(f"Total Inventory: {total_units} units")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History: {history}")

def display_inventory(total, history):
    print("\nCurrent Inventory:")
    print(f"Total: {total} units")
    for i, amount in enumerate(history, start=1):
        print(f"{i}, Delivery, {amount}")


def main():
    inventory, transaction_history = load_inventory()
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
        display_inventory(inventory, transaction_history)
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
            save_inventory(inventory, transaction_history)
            print("\nInventory successfully saved to inventory.txt")
            generate_report(inventory, failed_entries, deliveries_processed, transaction_history)
            print(f"Limit to overstocking: {limit - inventory} units")
            break

        if user_input is None:
            failed_entries += 1
            print(f"Times of Error: {failed_entries}")
            continue

        # Process valid delivery
        inventory = process_delivery(inventory, user_input)
        deliveries_processed += 1
        transaction_history.append(user_input)
        print(f"\nNew Delivery Added:\n{len(transaction_history)}, Delivery, {user_input}")
        tax = calculate_tax(user_input)
        failed_entries = 0 #Reset after a good entry

        print(f"✅ Inventory updated. Current total: {inventory} units")
        print(f"💰 Tax on this delivery: {tax:.2f}")
        print(f"Limit to overstocking: {limit - inventory} units")

        # Check for overstock
        if inventory > limit:
            print(f"⚠️ ALERT: Inventory exceeds {limit} units! Overstock detected. Resetting inventory to 0.")
            inventory = 0
            save_inventory(inventory, transaction_history)
            break

        # Warning when close to limit
        if inventory >= limit - amount:
            print(f"⚠️ ALERT: Inventory is close to limit! Units left before reaching {limit}: {limit - inventory}")


if __name__ == "__main__":
    main()
