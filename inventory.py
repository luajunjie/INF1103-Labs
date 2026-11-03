class Inventory:
    """Responsibility: manage a COLLECTION of Product objects (and their delivery records)."""

    def __init__(self):
        self.__products = []
        self.__history = []

    def add_product(self, product):
        """Add a Product object. Rejects duplicate names or IDs."""
        if self.search_product(product.get_name()) is not None:
            return False
        if self.search_by_id(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, name, partial=False):
        name = name.strip().lower()
        if name == "":
            return None
        for p in self.__products:
            stored = p.get_name().strip().lower()
            if stored == name or (partial and name in stored):
                return p
        return None

    def search_by_id(self, product_id):
        for p in self.__products:
            if p.get_product_id().lower() == product_id.strip().lower():
                return p
        return None

    def get_products(self):
        return list(self.__products)  # a copy, so outside code can't change our list

    def generate_next_id(self):
        return f"P{len(self.__products) + 1:03d}"

    def get_total(self):
        total = 0
        for p in self.__products:
            total += p.get_stock()
        return total

    def reset_all_stock(self):
        for p in self.__products:
            p.reset_stock()
            
    def record_delivery(self, product, amount, logged_by):
        """Ask the product to update its own stock, then log the delivery."""
        if not product.update_stock(amount):
            return False
        self.__history.append({"product": product.get_name(), "amount": amount, "logged_by": logged_by})
        return True

    def add_history_record(self, record):
        self.__history.append(record)

    def get_history(self):
        return list(self.__history)
    
        # ---- Display ----
    def display_all(self):
        print("\n📦 All Products:")
        if not self.__products:
            print("No products yet.")
        for p in self.__products:
            p.display_information()
        print(f"Total: {self.get_total()} units")

    def display_history(self):
        print("\n🧾 Past Deliveries:")
        if not self.__history:
            print("No deliveries recorded yet.")
            return
        for i, h in enumerate(self.__history, start=1):
            print(f"{i}. {h['product']} - {h['amount']} units, logged by {h.get('logged_by', 'unknown')}")
        print(f"Total deliveries on record: {len(self.__history)}")