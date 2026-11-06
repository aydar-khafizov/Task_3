import allure

from data import Ingredients
from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.profile_page import ProfilePage


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Клик по заказу открывает всплывающее окно с деталями")
    def test_order_modal_opens(self, driver, authorized_user):
        feed_page = OrderFeedPage(driver)
        feed_page.open()
        feed_page.click_first_order()
        assert feed_page.is_order_modal_opened(), "Модалка заказа не открылась"

    @allure.title("Заказы пользователя из истории отображаются в ленте")
    def test_order_from_history_in_feed(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.add_ingredient(Ingredients.BUN)
        main_page.add_ingredient(Ingredients.FILLING)
        main_page.click_place_order()

        assert main_page.is_order_modal_opened()
        order_number = main_page.wait_for_order_number()

        main_page.close_order_modal()
        main_page.click_profile()

        profile_page = ProfilePage(driver)
        profile_page.click_order_history_tab()

        main_page.wait_until_page_contains(order_number)
        main_page.click_order_feed()

        assert main_page.is_page_contains_text(order_number), f"Заказ {order_number} не найден в Ленте"

    @allure.title("Счётчик «Выполнено за всё время» увеличивается")
    def test_total_orders_counter_increases(self, driver, authorized_user):
        feed_page = OrderFeedPage(driver)
        feed_page.open()
        initial_count = feed_page.get_total_orders_count()

        main_page = MainPage(driver)
        main_page.click_constructor()
        main_page.add_ingredient(Ingredients.BUN)
        main_page.add_ingredient(Ingredients.FILLING)
        main_page.click_place_order()
        main_page.wait_for_order_number()
        main_page.close_order_modal()

        main_page.click_order_feed()

        feed_page.wait_for_total_counter_more_than(initial_count)
        new_count = feed_page.get_total_orders_count()
        assert new_count > initial_count

    @allure.title("Счётчик «Выполнено за сегодня» увеличивается")
    def test_today_orders_counter_increases(self, driver, authorized_user):
        feed_page = OrderFeedPage(driver)
        feed_page.open()
        initial_count = feed_page.get_today_orders_count()

        main_page = MainPage(driver)
        main_page.click_constructor()
        main_page.add_ingredient(Ingredients.BUN)
        main_page.add_ingredient(Ingredients.FILLING)
        main_page.click_place_order()
        main_page.wait_for_order_number()
        main_page.close_order_modal()

        main_page.click_order_feed()

        feed_page.wait_for_today_counter_more_than(initial_count)
        new_count = feed_page.get_today_orders_count()
        assert new_count > initial_count

    @allure.title("Номер заказа появляется в разделе «В работе»")
    def test_order_number_in_progress(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.add_ingredient(Ingredients.BUN)
        main_page.add_ingredient(Ingredients.FILLING)

        assert main_page.get_basket_items_count() > 0, "Корзина пуста! Drag-and-Drop не сработал."

        main_page.click_place_order()
        assert main_page.is_order_modal_opened()

        order_number = main_page.wait_for_order_number()

        main_page.close_order_modal()
        main_page.click_order_feed()

        feed_page = OrderFeedPage(driver)
        feed_page.wait_for_orders_loaded()

        normalized_order_number = str(int(order_number.replace("#", "").strip()))

        feed_page.wait_for_order_in_progress(normalized_order_number, timeout=30)

        in_progress = feed_page.get_in_progress_orders()
        assert normalized_order_number in in_progress, (
            f"Заказа {normalized_order_number} нет в разделе 'В работе'. "
            f"Текущие заказы: {in_progress}"
        )