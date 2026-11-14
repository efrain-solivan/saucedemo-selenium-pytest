import pytest

from pages.inventory_page import InventoryPage

BACKPACK = "Sauce Labs Backpack"
ONESIE = "Sauce Labs Onesie"


def _to_checkout(inventory, cart, *items):
    for name in items:
        inventory.add(name)
    inventory.open_cart()
    cart.checkout()


@pytest.mark.smoke
def test_checkout_end_to_end(inventory, cart, checkout):
    _to_checkout(inventory, cart, BACKPACK, ONESIE)
    checkout.fill("Efrain", "Solivan", "80233")
    subtotal, tax, total = checkout.amounts()
    assert subtotal == pytest.approx(29.99 + 7.99)
    assert total == pytest.approx(subtotal + tax, abs=0.01)
    assert checkout.finish() == "Thank you for your order!"
    assert inventory.cart_count() == 0


@pytest.mark.parametrize("first, last, postal, expected", [
    ("", "Solivan", "80233", "First Name is required"),
    ("Efrain", "", "80233", "Last Name is required"),
    ("Efrain", "Solivan", "", "Postal Code is required"),
], ids=["no-first-name", "no-last-name", "no-postal-code"])
def test_checkout_requires_every_field(inventory, cart, checkout, first, last, postal, expected):
    _to_checkout(inventory, cart, BACKPACK)
    checkout.fill(first, last, postal)
    assert expected in checkout.error_text()
    assert "checkout-step-one" in checkout.driver.current_url


def test_cancel_keeps_cart(inventory, cart, checkout):
    _to_checkout(inventory, cart, BACKPACK)
    checkout.click(checkout.CANCEL)
    assert cart.names() == [BACKPACK]


@pytest.mark.known_defect
@pytest.mark.xfail(strict=True, reason="problem_user: typing in Last Name overwrites First Name (seeded defect)")
def test_problem_user_last_name_field(login_page, cart, checkout):
    login_page.login("problem_user")
    inventory = InventoryPage(login_page.driver, login_page.base_url)
    assert inventory.is_loaded()
    _to_checkout(inventory, cart, BACKPACK)
    checkout.type(checkout.FIRST, "Efrain")
    checkout.type(checkout.LAST, "Solivan")
    assert checkout.field_value(checkout.LAST) == "Solivan"
