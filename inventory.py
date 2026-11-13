from product import Product

class Inventory:

    def __init__(self) -> None:
        self.__products: list[Product] = []
        self.__history: list[dict[str, str | int]] = []

    def add_product(self, product: Product) -> bool:
        if self.search_product(product.get_name()) is not None:
            return False
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def search_product(self, name: str, partial: bool = False) -> Product | None:
        name = name.strip().lower()
        if name == "":
            return None
        for p in self.__products:
            stored = p.get_name().strip().lower()
            if stored == name or (partial and name in stored):
                return p
        return None

    def remove_product(self, product_id: str) -> Product | None:
        product = self.find_product(product_id)
        if product is not None:
            self.__products.remove(product)
        return product

    def find_product(self, product_id: str) -> Product | None:
        for p in self.__products:
            if p.get_product_id().lower() == product_id.strip().lower():
                return p
        return None

    def get_products(self) -> list[Product]:
        return list(self.__products)  # a copy, so outside code can't change our list

    def generate_next_id(self) -> str:
        highest = 0
        for p in self.__products:
            digits = p.get_product_id()[1:]
            if digits.isdigit():
                highest = max(highest, int(digits))
        return f"P{highest + 1:03d}"

    def get_total(self) -> int:
        total = 0
        for p in self.__products:
            total += p.get_stock()
        return total

    def reset_all_stock(self) -> None:
        for p in self.__products:
            p.reset_stock()

    def record_delivery(self, product: Product, amount: int, logged_by: str) -> bool:         
        if not product.update_stock(amount):
            return False
        self.__history.append({"product": product.get_name(), "amount": amount, "logged_by": logged_by})
        return True

    def add_history_record(self, record: dict[str, str | int]) -> None:
        self.__history.append(record)

    def get_history(self) -> list[dict[str, str | int]]:
        return list(self.__history)
    
        # ---- Display ----
    def display_all(self) -> None:
        print("\n All Products:")
        if not self.__products:
            print("No products yet.")
        for p in self.__products:
            p.display_information()
        print(f"Total: {self.get_total()} units")

    def display_history(self) -> None:
        print("\n Past Deliveries:")
        if not self.__history:
            print("No deliveries recorded yet.")
            return
        for i, h in enumerate(self.__history, start=1):
            print(f"{i}. {h['product']} - {h['amount']} units, logged by {h.get('logged_by', 'unknown')}")
        print(f"Total deliveries on record: {len(self.__history)}")