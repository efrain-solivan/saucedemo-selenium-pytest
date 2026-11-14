import os
from pathlib import Path

import pytest
from selenium import webdriver

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage

BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")


def pytest_addoption(parser):
    parser.addoption("--headed", action="store_true", help="show the browser window")


@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    if not request.config.getoption("--headed"):
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1366,900")
    options.add_argument("--incognito")
    # Chrome's leaked-password dialog blocks the page after logging in with the public demo password.
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    drv = webdriver.Chrome(options=options)
    yield drv
    drv.quit()


@pytest.fixture
def login_page(driver):
    return LoginPage(driver, BASE_URL).open()


@pytest.fixture
def inventory(login_page):
    """Logged in as standard_user, on the product list."""
    login_page.login("standard_user")
    page = InventoryPage(login_page.driver, BASE_URL)
    assert page.is_loaded()
    return page


@pytest.fixture
def cart(driver):
    return CartPage(driver, BASE_URL)


@pytest.fixture
def checkout(driver):
    return CheckoutPage(driver, BASE_URL)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the HTML report when a test fails."""
    outcome = yield
    report = outcome.get_result()
    drv = item.funcargs.get("driver")
    if report.when == "call" and report.failed and drv is not None:
        shots = Path("reports/screenshots")
        shots.mkdir(parents=True, exist_ok=True)
        drv.save_screenshot(str(shots / f"{item.name}.png"))
        html = item.config.pluginmanager.getplugin("html")
        if html is not None:
            extras = getattr(report, "extras", [])
            extras.append(html.extras.png(drv.get_screenshot_as_base64()))
            report.extras = extras
