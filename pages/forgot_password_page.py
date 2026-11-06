from config import BASE_URL
from pages.base_page import BasePage
from locators.forgot_password_page_locators import ForgotPasswordPageLocators


class ForgotPasswordPage(BasePage):
    """Страница восстановления пароля (/forgot-password)."""

    def open(self):
        super().open(f"{BASE_URL}/forgot-password")

    def enter_email(self, email):
        self.send_keys(ForgotPasswordPageLocators.EMAIL_INPUT, email)

    def click_restore_button(self):
        self.click(ForgotPasswordPageLocators.RESTORE_BUTTON)

    def is_opened(self):
        return self.is_element_present(ForgotPasswordPageLocators.RESTORE_BUTTON)