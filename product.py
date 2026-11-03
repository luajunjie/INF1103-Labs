class Product:
    """Responsibility: represent and manage ONE product."""

    def __init__(self, product_id, name, price, stock=0):
        # Double underscore = "private" by convention (name mangling)
        self.__product_id = product_id
        self.__name = name
        self.__price = float(price)
        self.__stock = int(stock)

    def display_information(self):
        print(f"{self.__product_id} | {self.__name} | ${self.__price:.2f} | {self.__stock} units")