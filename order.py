from product import Product
from order_line import OrderLine
from discount_strategy import DiscountStrategy, NoDiscount


class Order:

    def __init__(self, order_id: str, discount: DiscountStrategy | None = None) -> None:
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        # The Order is GIVEN a strategy; it does not decide the discount itself
        self.__discount: DiscountStrategy = discount if discount is not None else NoDiscount()

    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

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
        total = sum(line.calculate_subtotal() for line in self.__order_lines)
        return self.__discount.apply(total)  # no if/elif: the strategy decides

    def display_information(self) -> None:
        print(f"\nOrder {self.__order_id}")
        if not self.__order_lines:
            print("  (no items)")
        for line in self.__order_lines:
            line.display_information()
        print(f"  Total: ${self.calculate_total():.2f}")