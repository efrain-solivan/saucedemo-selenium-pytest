import pytest


@pytest.mark.smoke
def test_standard_user_lands_on_products(inventory):
    assert inventory.names(), "product list is empty"


@pytest.mark.parametrize("username, password, expected", [
    ("locked_out_user", "secret_sauce", "Sorry, this user has been locked out."),
    ("standard_user", "wrong_password", "Username and password do not match any user in this service"),
    ("", "secret_sauce", "Username is required"),
    ("standard_user", "", "Password is required"),
], ids=["locked-out", "wrong-password", "empty-username", "empty-password"])
def test_login_rejected(login_page, username, password, expected):
    login_page.login(username, password)
    assert expected in login_page.error_text()
    assert login_page.driver.current_url.rstrip("/") == login_page.base_url.rstrip("/")


def test_logout_returns_to_login(inventory, login_page):
    inventory.logout()
    assert login_page.find(login_page.LOGIN_BUTTON).is_displayed()


def test_inventory_blocked_without_login(login_page):
    login_page.driver.get(login_page.base_url + "inventory.html")
    assert "when you are logged in" in login_page.error_text()
