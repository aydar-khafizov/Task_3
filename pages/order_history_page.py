from pages.base_page import BasePage


class OrderHistoryPage(BasePage):
    """Страница истории заказов (/account/order-history)."""

    def is_opened(self):
        try:
            self.wait_until_url_contains("/account/order-history")
            return True
        except Exception:
            return False