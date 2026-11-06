from product import Product


class DigitalProduct(Product):
    TYPE = "digital"

    def __init__(self, product_id, name, price, stock=0, download_size=0.0):
        super().__init__(product_id, name, price, stock)
        self.__download_size = float(download_size)

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print(f"    Type: Digital | Download size: {self.__download_size:.1f} MB")

    def to_dict(self):
        data = super().to_dict()
        data["type"] = self.TYPE
        data["download_size"] = self.__download_size
        return data
    
    def get_fulfilment_info(self):
        return f"{self.get_name()} is delivered digitally via a download link."