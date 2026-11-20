"""Lab 9 automated tests - run with:  python -m pytest"""
import ast
import inspect
from pathlib import Path

import pytest

import main
from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order
from order_line import OrderLine
from product_factory import ProductFactory
from file_handler import load_products
from discount_strategy import (DiscountStrategy, NoDiscount, PercentageDiscount,
                               BulkDiscount, StudentDiscount)

PROJECT_DIR = Path(__file__).resolve().parent.parent


# ---------- Fixtures ----------
@pytest.fixture
def supplier() -> Supplier:
    return Supplier("S001", "TechSource Pte Ltd", "sales@techsource.example")


@pytest.fixture
def order_of_250(supplier: Supplier) -> Order:
    """An order whose lines add up to 250 (2 x 100 + 1 x 50)."""
    order = Order("O001")
    order.add_order_line(ProductFactory.create("physical", "P001", "Desk", 100.00, 10, supplier), 2)
    order.add_order_line(ProductFactory.create("digital", "D001", "App", 50.00, 10, supplier), 1)
    return order


# ---------- Section 2: Strategy pattern ----------
def test_order_defaults_to_no_discount(order_of_250: Order) -> None:
    assert isinstance(order_of_250.get_discount(), NoDiscount)
    assert order_of_250.calculate_total() == pytest.approx(250)


@pytest.mark.parametrize("strategy, expected", [
    (NoDiscount(), 250),
    (PercentageDiscount(10), 225),
    (BulkDiscount(200, 20), 230),
    (StudentDiscount(), 237.5),
])
def test_order_total_uses_given_strategy(supplier: Supplier, strategy: DiscountStrategy,
                                         expected: float) -> None:
    order = Order("O002", strategy)
    order.add_order_line(ProductFactory.create("physical", "P001", "Desk", 125.00, 10, supplier), 2)
    assert order.calculate_total() == pytest.approx(expected)


def test_bulk_discount_not_applied_below_threshold() -> None:
    assert BulkDiscount(200, 20).apply(199.99) == pytest.approx(199.99)
    assert BulkDiscount(200, 20).apply(200) == pytest.approx(180)


def test_set_discount_changes_strategy_on_existing_order(order_of_250: Order) -> None:
    order_of_250.set_discount(BulkDiscount(200, 20))
    assert order_of_250.calculate_total() == pytest.approx(230)
    order_of_250.set_discount(PercentageDiscount(10))
    assert order_of_250.calculate_total() == pytest.approx(225)


def test_new_strategy_works_without_changing_order(order_of_250: Order) -> None:
    class HalfPriceDiscount(DiscountStrategy):  # brand-new strategy, defined only in this test
        def apply(self, total: float) -> float:
            return total / 2

    order_of_250.set_discount(HalfPriceDiscount())
    assert order_of_250.calculate_total() == pytest.approx(125)


def test_order_has_no_discount_if_elif_logic() -> None:
    # Parse the real code (comments are ignored) and look for any if/elif or "x if y else z"
    tree = ast.parse(inspect.getsource(Order.calculate_total).strip())
    assert not any(isinstance(node, (ast.If, ast.IfExp)) for node in ast.walk(tree))


def test_discount_strategy_is_abstract() -> None:
    with pytest.raises(TypeError):
        DiscountStrategy()


# ---------- Section 3: Factory pattern ----------
def test_factory_creates_physical_product(supplier: Supplier) -> None:
    product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier, 1.5)
    assert isinstance(product, PhysicalProduct)
    assert isinstance(product, Product)
    assert product.get_weight() == pytest.approx(1.5)


def test_factory_creates_digital_product(supplier: Supplier) -> None:
    product = ProductFactory.create("digital", "D001", "Photo Editor", 49.90, 100, supplier, 350)
    assert isinstance(product, DigitalProduct)
    assert product.get_download_size() == pytest.approx(350)


def test_factory_unknown_type_raises_clear_value_error(supplier: Supplier) -> None:
    with pytest.raises(ValueError, match="Unknown product type: service"):
        ProductFactory.create("service", "S001", "Installation", 30.00, 5, supplier)


@pytest.mark.parametrize("filename", ["main.py", "file_handler.py"])
def test_program_creates_products_through_factory(filename: str) -> None:
    source = (PROJECT_DIR / filename).read_text(encoding="utf-8")
    assert "PhysicalProduct(" not in source
    assert "DigitalProduct(" not in source
    assert "ProductFactory.create(" in source


# ---------- Section 4: Validation ----------
@pytest.mark.parametrize("price", [0, -5])
def test_invalid_price_is_rejected(supplier: Supplier, price: float) -> None:
    with pytest.raises(ValueError, match="Price must be greater than zero"):
        ProductFactory.create("physical", "P001", "Desk Lamp", price, 10, supplier)


@pytest.mark.parametrize("product_type", ["physical", "digital"])
def test_negative_stock_is_rejected_for_every_subclass(supplier: Supplier, product_type: str) -> None:
    with pytest.raises(ValueError, match="Stock quantity cannot be negative"):
        ProductFactory.create(product_type, "P001", "Desk Lamp", 25.00, -1, supplier)


def test_zero_stock_is_allowed(supplier: Supplier) -> None:
    product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 0, supplier)
    assert product.get_stock() == 0


@pytest.mark.parametrize("quantity", [0, -2])
def test_invalid_order_quantity_is_rejected(supplier: Supplier, quantity: int) -> None:
    product = ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier)
    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        OrderLine(product, quantity)


# ---------- Section 5.1: User input ----------
def test_get_positive_float_asks_again_until_valid(monkeypatch: pytest.MonkeyPatch,
                                                   capsys: pytest.CaptureFixture[str]) -> None:
    answers = iter(["abc", "-5", "12.50"])
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))

    assert main.get_positive_float("Price: ") == pytest.approx(12.50)
    output = capsys.readouterr().out.splitlines()
    assert output == ["Please enter a valid number, e.g. 12.50",
                      "Please enter a number greater than zero."]


def test_order_menu_asks_again_after_invalid_quantity(monkeypatch: pytest.MonkeyPatch,
                                                      capsys: pytest.CaptureFixture[str],
                                                      supplier: Supplier) -> None:
    inventory = Inventory()
    inventory.add_product(ProductFactory.create("physical", "P001", "Desk Lamp", 25.00, 10, supplier))
    answers = iter(["1", "0", "2", "n"])  # product 1, quantity 0 (rejected), quantity 2, no more
    monkeypatch.setattr("builtins.input", lambda prompt="": next(answers))

    orders: list[Order] = []
    assert main.create_order_menu(inventory, orders) is True
    assert "Quantity must be greater than zero" in capsys.readouterr().out
    assert orders[0].get_order_lines()[0].get_quantity() == 2


# ---------- Section 5.2: Loading products from a file ----------
def test_load_products_from_lab_csv(supplier: Supplier, capsys: pytest.CaptureFixture[str]) -> None:
    inventory = Inventory()
    load_products(str(PROJECT_DIR / "products.csv"), inventory, supplier)
    output = capsys.readouterr().out

    ids = [p.get_product_id() for p in inventory.get_products()]
    assert ids == ["P001", "D001", "P003"]               # valid rows still load
    assert "Unknown product type: service" in output     # bad rows are reported...
    assert "could not convert string to float: 'abc'" in output
    assert output.index("3 products loaded.") < output.index("Load attempt finished.")


def test_load_products_missing_file(supplier: Supplier, capsys: pytest.CaptureFixture[str],
                                    tmp_path: Path) -> None:
    inventory = Inventory()
    missing = tmp_path / "does_not_exist.csv"
    load_products(str(missing), inventory, supplier)  # must not crash
    output = capsys.readouterr().out

    assert f"Products file not found: {missing}" in output
    assert "products loaded" not in output            # else block did not run
    assert "Load attempt finished." in output         # finally always runs
    assert inventory.get_products() == []


def test_load_products_skips_bad_row_and_keeps_loading(supplier: Supplier, tmp_path: Path,
                                                       capsys: pytest.CaptureFixture[str]) -> None:
    csv_file = tmp_path / "products.csv"
    csv_file.write_text("product_type,product_id,name,price,stock_quantity\n"
                        "physical,P001,Desk Lamp,-1,10\n"       # invalid price
                        "digital,D001,Photo Editor,49.90,100\n")
    inventory = Inventory()
    load_products(str(csv_file), inventory, supplier)

    assert [p.get_product_id() for p in inventory.get_products()] == ["D001"]
    assert "1 products loaded." in capsys.readouterr().out


# ---------- Each except catches a specific exception ----------
@pytest.mark.parametrize("filename", ["main.py", "file_handler.py", "product_factory.py",
                                      "order.py", "order_line.py", "product.py"])
def test_no_bare_or_broad_except(filename: str) -> None:
    tree = ast.parse((PROJECT_DIR / filename).read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            assert node.type is not None, f"bare except in {filename}"
            assert ast.unparse(node.type) not in ("Exception", "BaseException"), \
                f"broad except in {filename}"
