from selenium.webdriver.common.by import By


class OrderHistoryLocators:
    ORDER_HISTORY_TAB_ACTIVE = (
        By.XPATH,
        "//a[@href='/account/order-history' and contains(@class, 'Account_link_active')]",
    )