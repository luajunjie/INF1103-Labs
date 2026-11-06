from product import Product
from can_be_shipped import CanBeShipped


class PhysicalProduct(Product, CanBeShipped):

    TYPE = "physical"
    BASE_SHIPPING = 5.00   # flat fee per item, in dollars
    RATE_PER_KG = 2.00     # extra charge per kilogram

    def __init__(self, product_id, name, price, stock=0, weight=0.0):
        super().__init__(product_id, name, price, stock)  # reuse Product's constructor
        self.__weight = float(weight)

    def get_weight(self):
        return self.__weight

    # ---- Overriding: reuse the parent's output, then add our own ----
    def display_information(self):
        super().display_information()
        print(f"    Type: Physical | Weight: {self.__weight:.2f} kg | "
              f"Shipping: ${self.calculate_shipping_cost():.2f}")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.TYPE
        data["weight"] = self.__weight
        return data

    # ---- Required by the abstract Product class ----
    def get_fulfilment_info(self):
        return f"{self.get_name()} requires physical shipping."

    # ---- Required by the CanBeShipped interface ----
    def calculate_shipping_cost(self):
        return self.BASE_SHIPPING + self.RATE_PER_KG * self.__weight