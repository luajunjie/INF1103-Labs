
def main():
    inventory = 0  # Initialize inventory to zero
    limit = 5000 # Set a stocking limit; can be customised anytime :)
    warning = 0.5 # Set a warning limit everytime the stock is about to reach this limit (this is in terms of %)
    amount = warning * limit # Visible amount of quantity left to stock limit
    approved_username = ['employee', 'manager', 'boss']
    failed_entries = 0
    user_auth = input("Enter username for authentication please: ")

    # User authentication
    if user_auth in approved_username:
        print(f"✅Access successful! Please continue. Currently logged in as:{user_auth}")
        
    else:
        print("Access unauthorized. Ending programme.")
        exit()

    while True: 
         
        user_input = input("Enter stock quantity (or type 'quit' to exit): ") 

        #Test number of times that user has failed his/her inputs
        if failed_entries == 3:
                     print("❌ You have entered in error 3 times. Exiting programme.")
                     break   

        # Check if user wants to quit
        if user_input.lower() == "quit":
            print(f"Final Inventory Report: {inventory} units")
            print(f"Limit to overstocking:{limit-inventory} units")
            break

        # Validate input: must be digits
        if not user_input.isdigit():
            print("❌ Error: Please enter a valid integer.")
            failed_entries +=1
            print(f"Times of Error: {failed_entries} ")
            continue

        # Convert to integer
        stock = int(user_input)

        # Reject negative numbers
        if stock < 0:
            print("❌ Error: Negative values are not allowed.")
            failed_entries +=1
            print(f"Times of Error: {failed_entries} ")
            continue

        # Update inventory
        inventory += stock
        print(f"✅ Inventory updated. Current total: {inventory} units")
        print(f"Limit to overstocking:{limit-inventory} units")

        # Check for overstock
        if inventory > limit:
            print(f"⚠️ ALERT: Inventory exceeds {limit} units! Overstock detected. Exiting programme and reinitializing back to 0.")
            break

  
   

if __name__ == "__main__":
    main()
