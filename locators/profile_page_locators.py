from selenium.webdriver.common.by import By


class ProfilePageLocators:
    ORDER_HISTORY_TAB = (By.XPATH, "//a[@href='/account/order-history']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")