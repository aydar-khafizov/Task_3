from config import BASE_URL
from pages.base_page import BasePage
from locators.profile_page_locators import ProfilePageLocators


class ProfilePage(BasePage):
    def is_opened(self):
        try:
            self.wait_until_url_contains("/account/profile")
            return True
        except Exception:
            return False

    def is_order_history_opened(self):
        try:
            self.wait_until_url_contains("/account/order-history")
            return True
        except Exception:
            return False

    def is_login_page_opened(self):
        try:
            self.wait_until_url_contains("/login")
            return True
        except Exception:
            return False

    def click_order_history_tab(self):
        self.click(ProfilePageLocators.ORDER_HISTORY_TAB)

    def click_logout(self):
        element = self.find_element(ProfilePageLocators.LOGOUT_BUTTON)
        self.execute_script("arguments[0].click();", element)