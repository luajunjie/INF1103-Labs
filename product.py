class Product:
    """Responsibility: represent and manage ONE product."""

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
        """Add (or remove, if negative) stock. Refuses to go below 0."""
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