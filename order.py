from product import Product
from order_line import OrderLine


class Order:

    def __init__(self, order_id: str) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []

    def get_order_id(self) -> str:
        return self.__order_id

    def add_order_line(self, product: Product, quantity: int) -> None:
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.__order_lines:
            if line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return list(self.__order_lines)  # a copy, so lines can't be added from outside

    def calculate_total(self) -> float:
        total = 0.0
        for line in self.__order_lines:
            total += line.calculate_subtotal()  # each line calculates its own subtotal
        return total

    def display_information(self) -> None:
        print(f"\n🧾 Order {self.__order_id}")
        if not self.__order_lines:
            print("  (no items)")
        for line in self.__order_lines:
            line.display_information()
        print(f"  Total: ${self.calculate_total():.2f}")