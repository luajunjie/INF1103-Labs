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


def generate_report(total_units, failed_attempts, deliveries_processed):
    print("\n📊 Final Inventory Report")
    print(f"Total Inventory: {total_units} units")
    print(f"Total Deliveries Processed: {deliveries_processed}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    inventory = 0
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
            generate_report(inventory, failed_entries, deliveries_processed)
            print(f"Limit to overstocking: {limit - inventory} units")
            break

        if user_input is None:
            failed_entries += 1
            print(f"Times of Error: {failed_entries}")
            continue

        # Process valid delivery
        inventory = process_delivery(inventory, user_input)
        deliveries_processed += 1
        tax = calculate_tax(user_input)

        print(f"✅ Inventory updated. Current total: {inventory} units")
        print(f"💰 Tax on this delivery: {tax:.2f}")
        print(f"Limit to overstocking: {limit - inventory} units")

        # Check for overstock
        if inventory > limit:
            print(f"⚠️ ALERT: Inventory exceeds {limit} units! Overstock detected. Resetting inventory to 0.")
            inventory = 0
            break

        # Warning when close to limit
        if inventory >= limit - amount:
            print(f"⚠️ ALERT: Inventory is close to limit! Units left before reaching {limit}: {limit - inventory}")


if __name__ == "__main__":
    main()
