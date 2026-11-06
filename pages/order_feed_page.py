from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.get_total_orders_count() > initial_count
        )

    def wait_for_today_counter_more_than(self, initial_count, timeout=15):
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.get_today_orders_count() > initial_count
        )

    def click_first_order(self):
        element = self.wait.until(EC.element_to_be_clickable(OrderFeedLocators.ORDER_CARD))
        self.execute_script("arguments[0].click();", element)

    def is_order_modal_opened(self):
        return self.is_element_visible(OrderFeedLocators.ORDER_MODAL)

    def get_order_number_from_modal(self):
        text = self.get_text(OrderFeedLocators.ORDER_MODAL_NUMBER)
        return text.replace("#", "").strip()

    def get_in_progress_orders(self):
        """
        Возвращает список номеров из раздела «В работе».
        """
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
        """Ждет до 30 секунд появления заказа в разделе «В работе»."""
        def check(driver):
            try:
                return order_number in self.get_in_progress_orders()
            except StaleElementReferenceException:
                return False

        WebDriverWait(self.driver, timeout).until(check)