from product import Product
from supplier import Supplier
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


# ---------- Section 2: Association (Supplier and Product) ----------
print("=== 2. ASSOCIATION: Supplier and Product ===")
supplier = Supplier("S010", "Music World Pte Ltd", "hello@musicworld.example")
guitar = PhysicalProduct("P101", "Guitar", 350.00, 5, supplier, weight=3.5)
music_app = DigitalProduct("P102", "Music Studio App", 89.00, 50, supplier, download_size=1200)

print("Supplier, displayed through each product:")
guitar.get_supplier().display_information()
music_app.get_supplier().display_information()
print(f"Both products point to the same Supplier object? {guitar.get_supplier() is music_app.get_supplier()}")
print(f"The Supplier is a separate object from the Product? {guitar.get_supplier() is not guitar}")


del supplier
print("After `del supplier`, the products still reach their supplier:")
guitar.display_information()
music_app.display_information()



# ---------- Section 3: Aggregation (Inventory and Product) ----------
print("\n=== 3. AGGREGATION: Inventory and Product ===")
drum_supplier = Supplier("S011", "Beat Gear", "orders@beatgear.example")
drum = PhysicalProduct("P201", "Drum Kit", 899.00, 2, drum_supplier, weight=25.0)  # created BEFORE any inventory

inventory_a = Inventory()
inventory_b = Inventory()

inventory_a.add_product(drum)
print(f"In Inventory A? {inventory_a.find_product('P201') is drum}")


removed = inventory_a.remove_product("P201")
print(f"Removed from A. Still in Inventory A? {inventory_a.find_product('P201') is not None}")
print(f"The removed product is the same object? {removed is drum}")
print("The product still works after removal:")
drum.display_information()
drum.update_stock(3)
print(f"Stock updated after removal: {drum.get_stock()} units")

inventory_b.add_product(drum)
print(f"Same object added to Inventory B? {inventory_b.find_product('P201') is drum}")
print(f"find_product for a missing ID returns: {inventory_b.find_product('P999')}")


# ---------- Section 4: Composition (Order and OrderLine) ----------
print("\n=== 4. COMPOSITION: Order and OrderLine ===")
order_1 = Order("O001")
order_1.add_order_line(guitar, 2)
order_1.add_order_line(music_app, 1)
order_1.display_information()


order_2 = Order("O002")
order_2.add_order_line(guitar, 1)
line_in_order_1 = order_1.get_order_lines()[0]
line_in_order_2 = order_2.get_order_lines()[0]
print(f"\nSame OrderLine object in both orders? {line_in_order_1 is line_in_order_2}")
print(f"Same Product object in both lines? {line_in_order_1.get_product() is line_in_order_2.get_product()}")
print(f"OrderLine ids: {id(line_in_order_1)} vs {id(line_in_order_2)} (different)")
print(f"Product ids:   {id(line_in_order_1.get_product())} vs {id(line_in_order_2.get_product())} (same)")

order_1.remove_order_line("P102")
print("\nAfter removing the Music Studio App line from O001:")
order_1.display_information()
print("The product itself still exists:", music_app.get_name())


# ---------- Section 6: LSP----------
print("\n=== 6. LSP: any Product can be substituted ===")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


show_product_details(guitar)      # a PhysicalProduct
show_product_details(music_app)   # a DigitalProduct

print("\nupdate_stock() keeps the same meaning for both subclasses:")
for product in (guitar, music_app):
    before = product.get_stock()
    accepted = product.update_stock(4)
    rejected = product.update_stock(-1000)  # would go below 0
    print(f"  {product.get_name()}: {before} -> {product.get_stock()} "
          f"(+4 accepted: {accepted}, -1000 accepted: {rejected})")


# ---------- Section 7: Polymorphism through Product references ----------
print("\n=== 7. POLYMORPHISM: one loop, no isinstance() ===")
store = Inventory()
store.add_product(guitar)
store.add_product(music_app)
store.add_product(drum)

for product in store.get_products():
    product.display_information()
    print(f"    -> {product.get_fulfilment_info()}")

print("\n All Lab 8 tests ran.")