from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    ITEM_PRICES = (By.CSS_SELECTOR, "[data-test='inventory-item-price']")
    SORT = (By.CSS_SELECTOR, "[data-test='product-sort-container']")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    MENU = (By.ID, "react-burger-menu-btn")
    LOGOUT = (By.ID, "logout_sidebar_link")

    @staticmethod
    def _slug(name):
        return name.lower().replace(" ", "-")

    def is_loaded(self):
        self.wait_for_url("/inventory.html")
        return self.find(self.TITLE).text == "Products"

    def names(self):
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def prices(self):
        return [float(e.text.lstrip("$")) for e in self.find_all(self.ITEM_PRICES)]

    def sort_by(self, value):
        Select(self.find(self.SORT)).select_by_value(value)

    def add(self, name):
        self.click((By.ID, f"add-to-cart-{self._slug(name)}"))

    def remove(self, name):
        self.click((By.ID, f"remove-{self._slug(name)}"))

    def cart_count(self):
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        self.click(self.CART_LINK)

    def logout(self):
        self.click(self.MENU)
        self.click(self.LOGOUT)
