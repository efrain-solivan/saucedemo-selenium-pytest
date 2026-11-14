import pytest

from pages.inventory_page import InventoryPage


def test_catalog_has_six_products(inventory):
    assert len(inventory.names()) == 6


@pytest.mark.parametrize("option, key, reverse", [
    ("az", "names", False),
    ("za", "names", True),
    ("lohi", "prices", False),
    ("hilo", "prices", True),
])
def test_sort_orders_products(inventory, option, key, reverse):
    inventory.sort_by(option)
    values = getattr(inventory, key)()
    assert values == sorted(values, reverse=reverse)


@pytest.mark.known_defect
@pytest.mark.xfail(strict=True, reason="problem_user: sorting by price does not reorder the list (seeded defect)")
def test_problem_user_sort_by_price(login_page):
    login_page.login("problem_user")
    page = InventoryPage(login_page.driver, login_page.base_url)
    assert page.is_loaded()
    page.sort_by("lohi")
    prices = page.prices()
    assert prices == sorted(prices)
