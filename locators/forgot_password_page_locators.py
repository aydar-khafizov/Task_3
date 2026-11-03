from selenium.webdriver.common.by import By


class ForgotPasswordPageLocators:
    EMAIL_INPUT = (By.XPATH, "//input[@name='name']")
    RESTORE_BUTTON = (By.XPATH, "//button[text()='Восстановить']")

    # Поле пароля до активации (скрытый режим)
    PASSWORD_INPUT_BEFORE = (
        By.CSS_SELECTOR,
        "div.input.input_type_password",
    )
    # Поле пароля после активации (открытый режим)
    PASSWORD_INPUT_AFTER = (
        By.CSS_SELECTOR,
        "div.input.input_type_text.input_status_active",
    )
    # Кнопка переключения видимости пароля
    TOGGLE_PASSWORD_BUTTON = (
        By.CSS_SELECTOR,
        "div.input__icon.input__icon-action",
    )