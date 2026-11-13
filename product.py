from abc import ABC, abstractmethod
from supplier import Supplier

class Product(ABC):

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier) -> None:
        # Double underscore = "private" by convention (name mangling)
        self.__product_id: str = product_id
        self.__name: str = name
        self.__price: float = float(price)
        self.__stock: int = int(stock)
        self.__supplier: Supplier = supplier

    def get_product_id(self) -> str:
        return self.__product_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_stock(self) -> int:
        return self.__stock

    def get_supplier(self) -> Supplier:
        return self.__supplier

    def update_stock(self, quantity: int) -> bool:
        if not isinstance(quantity, int):
            return False
        if self.__stock + quantity < 0:
            return False
        self.__stock += quantity
        return True

    def reset_stock(self) -> None:
        self.__stock = 0    

    def display_information(self) -> None:
        print(f"{self.__product_id} | {self.__name} | ${self.__price:.2f} | {self.__stock} units")
        print(f"    Supplier: {self.__supplier.get_name()} ({self.__supplier.get_contact_email()})")

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }  

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass   