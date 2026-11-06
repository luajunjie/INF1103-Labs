class Product:

    def __init__(self, product_id, name, price, stock=0):
        # Double underscore = "private" by convention (name mangling)
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        if not isinstance(quantity, int):
            return False
        if self.__stock + quantity < 0:
            return False
        self.__stock += quantity
        return True

    def reset_stock(self):
        self.__stock = 0    

    def display_information(self):
        print(f"{self.__product_id} | {self.__name} | ${self.__price:.2f} | {self.__stock} units")

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }     