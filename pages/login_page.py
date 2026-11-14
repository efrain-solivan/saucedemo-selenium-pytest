from selenium.webdriver.common.by import By

from pages.base_page import BasePage

PASSWORD = "secret_sauce"  # public demo password published on saucedemo.com


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD_FIELD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")

    def open(self):
        self.driver.get(self.base_url)
        return self

    def login(self, username, password=PASSWORD):
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD_FIELD, password)
        self.click(self.LOGIN_BUTTON)
