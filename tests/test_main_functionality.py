import allure

from data import Ingredients, ExpectedValues
from pages.main_page import MainPage


@allure.feature("Основной функционал")
class TestMainFunctionality:

    @allure.title("Переход в раздел «Конструктор»")
    def test_go_to_constructor(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_order_feed()
        main_page.click_constructor()

        assert main_page.is_constructor_opened(), "Не открылся Конструктор"

    @allure.title("Переход в раздел «Лента заказов»")
    def test_go_to_order_feed(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_order_feed()

        assert main_page.is_order_feed_opened(), "Не открылась Лента заказов"

    @allure.title("Открытие всплывающего окна с деталями ингредиента")
    def test_ingredient_modal_opens(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_ingredient(Ingredients.BUN)

        assert main_page.is_ingredient_modal_opened(), "Модалка не открылась"

    @allure.title("Закрытие всплывающего окна кликом по крестику")
    def test_ingredient_modal_closes(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_ingredient(Ingredients.BUN)
        assert main_page.is_ingredient_modal_opened()

        main_page.close_ingredient_modal()
        assert main_page.is_ingredient_modal_closed(), "Модалка не закрылась"

    @allure.title("Счётчик ингредиента увеличивается при добавлении в заказ")
    def test_ingredient_counter_increases(self, driver, authorized_user):
        main_page = MainPage(driver)
        initial_counter = main_page.get_ingredient_counter(Ingredients.BUN)

        main_page.add_ingredient(Ingredients.BUN)
        new_counter = main_page.get_ingredient_counter(Ingredients.BUN)

        assert new_counter > initial_counter, (
            f"Счётчик не увеличился. Было {initial_counter}, стало {new_counter}"
        )

    @allure.title("Оформление заказа залогиненным пользователем")
    def test_place_order(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.open()

        main_page.add_ingredient(Ingredients.BUN)
        main_page.add_ingredient(Ingredients.FILLING)

        main_page.click_place_order()
        assert main_page.is_order_modal_opened()

        order_number = main_page.wait_for_order_number()

        assert order_number != ExpectedValues.ORDER_NUMBER_PLACEHOLDER, "Номер заказа не сгенерировался"