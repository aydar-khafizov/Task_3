from selenium.webdriver.common.by import By


class OrderFeedLocators:
    # Счётчики
    TOTAL_ORDERS_COUNTER = (By.XPATH, "//p[text()='Выполнено за все время:']/following-sibling::p[1]")
    TODAY_ORDERS_COUNTER = (By.XPATH, "//p[text()='Выполнено за сегодня:']/following-sibling::p[1]")

    # Карточка заказа в ленте
    ORDER_CARD = (By.XPATH, "//a[contains(@class, 'OrderHistory_link__')]")

    # Модалка заказа
    ORDER_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_orderBox__')]")
    ORDER_MODAL_NUMBER = (By.XPATH, "//div[contains(@class, 'Modal_orderBox__')]//p[contains(@class, 'text_type_digits-default')]")

    # Забираем все из блока статусов (и "Готовы", и "В работе")
    IN_PROGRESS_LIST = (By.XPATH, "//div[contains(@class, 'OrderFeed_orderStatusBox__')]//ul/li")