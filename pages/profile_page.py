from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage
from locators.profile_page_locators import ProfilePageLocators


class ProfilePage(BasePage):
    """Страница личного кабинета (/account/profile)."""

    def is_opened(self, timeout=10):
        """Ждет, пока URL сменится на /account/profile."""
        try:
            self.wait.until(EC.url_contains("/account/profile"))
            return True
        except Exception:
            return False

    def click_order_history_tab(self):
        self.click(ProfilePageLocators.ORDER_HISTORY_TAB)

    def click_logout(self):
        """Нажимает «Выход» через JS и ждет редиректа на логин."""
        element = self.find_element(ProfilePageLocators.LOGOUT_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)
        # Ждем, пока URL сменится на /login
        self.wait.until(EC.url_contains("/login"))