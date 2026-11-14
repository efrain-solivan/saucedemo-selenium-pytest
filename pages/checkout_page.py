import re

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


def _money(text):
    return float(re.search(r"\$([\d.]+)", text).group(1))


class CheckoutPage(BasePage):
    FIRST = (By.ID, "first-name")
    LAST = (By.ID, "last-name")
    POSTAL = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    CANCEL = (By.ID, "cancel")
    SUBTOTAL = (By.CSS_SELECTOR, "[data-test='subtotal-label']")
    TAX = (By.CSS_SELECTOR, "[data-test='tax-label']")
    TOTAL = (By.CSS_SELECTOR, "[data-test='total-label']")
    FINISH = (By.ID, "finish")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")

    def fill(self, first, last, postal):
        self.type(self.FIRST, first)
        self.type(self.LAST, last)
        self.type(self.POSTAL, postal)
        self.click(self.CONTINUE)

    def field_value(self, locator):
        return self.find(locator).get_attribute("value")

    def amounts(self):
        self.wait_for_url("/checkout-step-two.html")
        return (_money(self.find(self.SUBTOTAL).text),
                _money(self.find(self.TAX).text),
                _money(self.find(self.TOTAL).text))

    def finish(self):
        self.click(self.FINISH)
        return self.find(self.COMPLETE_HEADER).text
