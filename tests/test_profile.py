import allure

from pages.main_page import MainPage
from pages.profile_page import ProfilePage


@allure.feature("Личный кабинет")
class TestProfile:

    @allure.title("Переход в личный кабинет")
    def test_go_to_profile(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_profile()
        
        profile_page = ProfilePage(driver)
        assert profile_page.is_opened(), "Не открылась страница профиля"

    @allure.title("Переход в историю заказов")
    def test_go_to_order_history(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_profile()
        
        profile_page = ProfilePage(driver)
        profile_page.click_order_history_tab()
        
        assert "/account/order-history" in driver.current_url, "Не открылась история заказов"

    @allure.title("Выход из аккаунта")
    def test_logout(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.click_profile()
        
        profile_page = ProfilePage(driver)
        profile_page.click_logout()
        
        assert "/login" in driver.current_url, "Не произошел выход из аккаунта"