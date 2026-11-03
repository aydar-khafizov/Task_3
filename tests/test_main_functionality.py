import allure
import time
from pages.main_page import MainPage

@allure.feature("Основной функционал")
class TestMainFunctionality:

    @allure.title("Переход в Конструктор")
    def test_go_to_constructor(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_order_feed()
        main_page.click_constructor()
        assert driver.current_url.endswith("/")

    @allure.title("Переход в Ленту заказов")
    def test_go_to_order_feed(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_order_feed()
        assert "/feed" in driver.current_url

    @allure.title("Открытие и закрытие модалки ингредиента")
    def test_ingredient_modal(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_ingredient("Флюоресцентная булка R2-D3")
        assert main_page.is_ingredient_modal_opened()
        
        main_page.close_ingredient_modal()
        assert main_page.is_ingredient_modal_closed()

    @allure.title("Увеличение счетчика ингредиента")
    def test_ingredient_counter(self, driver, authorized_user):
        main_page = MainPage(driver)
        ingredient = "Флюоресцентная булка R2-D3"
        
        initial = main_page.get_ingredient_counter(ingredient)
        main_page.add_ingredient(ingredient)
        new_count = main_page.get_ingredient_counter(ingredient)
        
        assert new_count > initial

    @allure.title("Оформление заказа авторизованным юзером")
    def test_place_order(self, driver, authorized_user):
        main_page = MainPage(driver)
        
        main_page.add_ingredient("Флюоресцентная булка R2-D3")
        time.sleep(0.5)
        main_page.add_ingredient("Мясо бессмертных моллюсков Protostomia")
        time.sleep(0.5)
        
        main_page.click_place_order()
        assert main_page.is_order_modal_opened()
        
        order_number = main_page.wait_for_order_number()
        assert order_number != "9999"