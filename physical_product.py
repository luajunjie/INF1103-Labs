from product import Product
from supplier import Supplier
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):

    TYPE: str = "physical"
    BASE_SHIPPING: float = 5.00   # flat fee per item, in dollars
    RATE_PER_KG: float = 2.00     # extra charge per kilogram

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, weight: float = 0.0) -> None:
        super().__init__(product_id, name, price, stock, supplier)  # reuse Product's constructor
        self.__weight: float = float(weight)

    def get_weight(self) -> float:
        return self.__weight

    # ---- Overriding: reuse the parent's output, then add our own ----
    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg | "
              f"Shipping: ${self.calculate_shipping_cost():.2f}")

    def to_dict(self) -> dict[str, str | float]:
        data = super().to_dict()
        data["type"] = self.TYPE
        data["weight"] = self.__weight
        return data

    # ---- Required by the abstract Product class ----
    def get_fulfilment_info(self) -> str:
        return f"{self.get_name()} requires physical shipping."

    # ---- Required by the CanBeShipped interface ----
    def calculate_shipping_cost(self) -> float:
        return self.BASE_SHIPPING + self.RATE_PER_KG * self.__weight