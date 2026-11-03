from pages.base_page import BasePage
from locators.reset_password_page_locators import ResetPasswordPageLocators

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class ResetPasswordPage(BasePage):
    """Страница сброса пароля (/reset-password)."""

    def open(self):
        super().open(f"{BASE_URL}/reset-password")

    def click_show_hide_password(self):
        self.click(ResetPasswordPageLocators.SHOW_HIDE_PASSWORD_BUTTON)

    def is_opened(self):
        return self.is_element_present(ResetPasswordPageLocators.PASSWORD_INPUT)

    def is_password_field_active(self):
        """Активно ли поле пароля (подсвечено после клика по глазику)."""
        return self.is_element_present(ResetPasswordPageLocators.ACTIVE_PASSWORD_FIELD)