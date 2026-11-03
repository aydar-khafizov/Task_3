from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from locators.order_feed_locators import OrderFeedLocators

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class OrderFeedPage(BasePage):
    """Страница Ленты заказов (/feed)."""

    def open(self):
        super().open(f"{BASE_URL}/feed")
        # Увеличили ожидание загрузки счётчиков до 20 секунд
        WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located(OrderFeedLocators.TOTAL_ORDERS_COUNTER)
        )

    def get_total_orders_count(self):
        text = self.get_text(OrderFeedLocators.TOTAL_ORDERS_COUNTER)
        return int(text)

    def get_today_orders_count(self):
        text = self.get_text(OrderFeedLocators.TODAY_ORDERS_COUNTER)
        return int(text)

    def click_first_order(self):
        element = self.find_element(OrderFeedLocators.ORDER_CARD)
        self.driver.execute_script("arguments[0].click();", element)

    def is_order_modal_opened(self):
        return self.is_element_visible(OrderFeedLocators.ORDER_MODAL)

    def get_order_number_from_modal(self):
        text = self.get_text(OrderFeedLocators.ORDER_MODAL_NUMBER)
        return text.replace("#", "").strip()

    def get_in_progress_orders(self):
        elements = self.driver.find_elements(*OrderFeedLocators.IN_PROGRESS_LIST)
        result = []
        for el in elements:
            text = el.text.strip().replace("#", "")
            if text.isdigit():
                result.append(str(int(text)))
        return result