from pages.base_page import BasePage


class OrderHistoryPage(BasePage):
    """Страница истории заказов (/account/order-history)."""

    def is_opened(self):
        """Проверяем URL."""
        return "/account/order-history" in self.driver.current_url