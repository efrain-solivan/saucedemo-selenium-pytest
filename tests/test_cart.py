import pytest

BACKPACK = "Sauce Labs Backpack"
BIKE_LIGHT = "Sauce Labs Bike Light"


@pytest.mark.smoke
def test_add_item_updates_badge_and_cart(inventory, cart):
    inventory.add(BACKPACK)
    assert inventory.cart_count() == 1
    inventory.open_cart()
    assert cart.names() == [BACKPACK]


def test_remove_item_from_inventory(inventory, cart):
    inventory.add(BACKPACK)
    inventory.add(BIKE_LIGHT)
    inventory.remove(BACKPACK)
    assert inventory.cart_count() == 1
    inventory.open_cart()
    assert cart.names() == [BIKE_LIGHT]


def test_cart_survives_navigation(inventory, cart):
    inventory.add(BACKPACK)
    inventory.open_cart()
    cart.click(cart.CONTINUE_SHOPPING)
    assert inventory.is_loaded()
    assert inventory.cart_count() == 1


def test_empty_cart_has_no_badge(inventory):
    assert inventory.cart_count() == 0
