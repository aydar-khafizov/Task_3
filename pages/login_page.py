from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class LoginPage(BasePage):
    """Страница авторизации (/login)."""

    def open(self):
        super().open(f"{BASE_URL}/login")

    def login(self, email, password):
        self.send_keys(LoginPageLocators.EMAIL_INPUT, email)
        self.send_keys(LoginPageLocators.PASSWORD_INPUT, password)

        # Даём React время обработать input-события (как в debug_login.py)
        self.find_element(LoginPageLocators.EMAIL_INPUT).get_attribute("value")
        self.find_element(LoginPageLocators.PASSWORD_INPUT).get_attribute("value")

        self.click_login_button()

    def click_login_button(self):
        """Кликает по кнопке Войти"""
        self.wait.until(
            EC.presence_of_element_located(LoginPageLocators.LOGIN_BUTTON)
        )
        buttons = self.driver.find_elements(*LoginPageLocators.LOGIN_BUTTON)
        for btn in buttons:
            if btn.is_displayed():
                self.driver.execute_script("arguments[0].click();", btn)
                return

    def click_forgot_password_link(self):
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)

    def click_register_link(self):
        self.click(LoginPageLocators.REGISTER_LINK)

    def is_opened(self):
        return self.is_element_present(LoginPageLocators.LOGIN_BUTTON)