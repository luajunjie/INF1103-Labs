from product import Product
from supplier import Supplier


class DigitalProduct(Product):
    TYPE: str = "digital"

    def __init__(self, product_id: str, name: str, price: float, stock: int,
                 supplier: Supplier, download_size: float = 0.0) -> None:
        super().__init__(product_id, name, price, stock, supplier)  # reuse Product's constructor
        self.__download_size: float = float(download_size)

    def get_download_size(self) -> float:
        return self.__download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"    Type: Digital | Download size: {self.__download_size:.1f} MB")

    def to_dict(self) -> dict[str, str | float]:
        data = super().to_dict()
        data["type"] = self.TYPE
        data["download_size"] = self.__download_size
        return data
    
    def get_fulfilment_info(self) -> str:
        return f"{self.get_name()} is delivered digitally via a download link."