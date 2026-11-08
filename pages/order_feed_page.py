from selenium.common.exceptions import StaleElementReferenceException

from config import BASE_URL
from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators


class OrderFeedPage(BasePage):
    def open(self):
        super().open(f"{BASE_URL}/feed")
        self.wait_until_visible(OrderFeedLocators.TOTAL_ORDERS_COUNTER, timeout=20)

    def wait_for_orders_loaded(self, timeout=20):
        self.wait_until_visible(OrderFeedLocators.TOTAL_ORDERS_COUNTER, timeout=timeout)

    def get_total_orders_count(self):
        text = self.get_text(OrderFeedLocators.TOTAL_ORDERS_COUNTER)
        return int(text)

    def get_today_orders_count(self):
        text = self.get_text(OrderFeedLocators.TODAY_ORDERS_COUNTER)
        return int(text)

    def wait_for_total_counter_more_than(self, initial_count, timeout=15):
        # Используем wait_until из BasePage
        self.wait_until(lambda d: self.get_total_orders_count() > initial_count, timeout)

    def wait_for_today_counter_more_than(self, initial_count, timeout=15):
        # Используем wait_until из BasePage
        self.wait_until(lambda d: self.get_today_orders_count() > initial_count, timeout)

    def click_first_order(self):
        # Используем click_js из BasePage
        self.click_js(OrderFeedLocators.ORDER_CARD)

    def is_order_modal_opened(self):
        return self.is_element_visible(OrderFeedLocators.ORDER_MODAL)

    def get_order_number_from_modal(self):
        text = self.get_text(OrderFeedLocators.ORDER_MODAL_NUMBER)
        return text.replace("#", "").strip()

    def get_in_progress_orders(self):
        result = []
        elements = self.find_elements(OrderFeedLocators.IN_PROGRESS_LIST)
        for el in elements:
            try:
                text = el.text.strip().replace("#", "")
                if text.isdigit():
                    result.append(str(int(text)))
            except StaleElementReferenceException:
                continue
        return result

    def wait_for_order_in_progress(self, order_number, timeout=30):
        def check(driver):
            try:
                return order_number in self.get_in_progress_orders()
            except StaleElementReferenceException:
                return False

        # Используем wait_until из BasePage
        self.wait_until(check, timeout)