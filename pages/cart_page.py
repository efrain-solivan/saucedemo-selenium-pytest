from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (By.CSS_SELECTOR, "[data-test='inventory-item-name']")
    CHECKOUT = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def names(self):
        self.wait_for_url("/cart.html")
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def checkout(self):
        self.click(self.CHECKOUT)
