from config import BASE_URL
from pages.base_page import BasePage
from locators.login_page_locators import LoginPageLocators


class LoginPage(BasePage):
    """Страница авторизации (/login)."""

    def open(self):
        super().open(f"{BASE_URL}/login")

    def login(self, email, password):
        self.send_keys(LoginPageLocators.EMAIL_INPUT, email)
        self.send_keys(LoginPageLocators.PASSWORD_INPUT, password)
        # Используем наш инкапсулированный метод
        self.click_js(LoginPageLocators.LOGIN_BUTTON)

    def click_forgot_password_link(self):
        self.click(LoginPageLocators.FORGOT_PASSWORD_LINK)

    def click_register_link(self):
        self.click(LoginPageLocators.REGISTER_LINK)

    def is_opened(self):
        return self.is_element_present(LoginPageLocators.LOGIN_BUTTON)