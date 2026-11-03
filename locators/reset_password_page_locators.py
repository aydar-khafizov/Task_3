from selenium.webdriver.common.by import By


class ResetPasswordPageLocators:
    # Поле "Введите новый пароль"
    PASSWORD_INPUT = (By.XPATH, "//input[@name='Введите новый пароль']")
    # Кнопка-глазик (показать/скрыть пароль)
    SHOW_HIDE_PASSWORD_BUTTON = (By.XPATH, "//div[contains(@class, 'input__icon-action')]")
    # Контейнер поля пароля в активном состоянии (подсвечен)
    ACTIVE_PASSWORD_FIELD = (By.XPATH, "//div[contains(@class, 'input_status_active')]")