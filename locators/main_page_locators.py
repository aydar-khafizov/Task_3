from selenium.webdriver.common.by import By


class MainPageLocators:
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, "//p[text()='Лента Заказов']")
    PROFILE_BUTTON = (By.XPATH, "//p[contains(text(), 'Личный')]")

    @staticmethod
    def INGREDIENT_IMAGE(name):
        return (By.XPATH, f"//img[@alt='{name}']")

    @staticmethod
    def INGREDIENT_COUNTER(name):
        return (
            By.XPATH,
            f"//img[@alt='{name}']/ancestor::*[contains(@class, 'BurgerIngredient_ingredient')][1]//p[contains(@class, 'counter_counter__num')]",
        )

    INGREDIENT_MODAL_TITLE = (By.XPATH, "//h2[text()='Детали ингредиента']")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")

    PLACE_ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    ORDER_NUMBER_MODAL = (By.XPATH, "//h2[contains(@class, 'text_type_digits-large')]")