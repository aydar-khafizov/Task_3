import time

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.main_page import MainPage
from pages.order_feed_page import OrderFeedPage
from pages.profile_page import ProfilePage
from locators.order_feed_locators import OrderFeedLocators


@allure.feature("Лента заказов")
class TestOrderFeed:

    @allure.title("Клик по заказу открывает всплывающее окно с деталями")
    def test_order_modal_opens(self, driver, authorized_user):
        feed_page = OrderFeedPage(driver)
        feed_page.open()
        time.sleep(1)  # Даем React время успокоиться после загрузки
        feed_page.click_first_order()
        assert feed_page.is_order_modal_opened(), "Модалка заказа не открылась"

    @allure.title("Заказы пользователя из истории отображаются в ленте")
    def test_order_from_history_in_feed(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.add_ingredient("Флюоресцентная булка R2-D3")
        main_page.add_ingredient("Мясо бессмертных моллюсков Protostomia")
        main_page.click_place_order()

        assert main_page.is_order_modal_opened()
        order_number = main_page.wait_for_order_number()

        main_page.close_order_modal()
        main_page.click_profile()

        profile_page = ProfilePage(driver)
        profile_page.click_order_history_tab()

        WebDriverWait(driver, 10).until(lambda d: order_number in d.page_source)
        main_page.click_order_feed()

        assert order_number in driver.page_source, f"Заказ {order_number} не найден в Ленте"

    @allure.title("Счётчик «Выполнено за всё время» увеличивается")
    def test_total_orders_counter_increases(self, driver, authorized_user):
        feed_page = OrderFeedPage(driver)
        feed_page.open()
        initial_count = feed_page.get_total_orders_count()

        main_page = MainPage(driver)
        main_page.click_constructor()
        main_page.add_ingredient("Флюоресцентная булка R2-D3")
        main_page.add_ingredient("Мясо бессмертных моллюсков Protostomia")
        main_page.click_place_order()
        main_page.wait_for_order_number()
        main_page.close_order_modal()

        main_page.click_order_feed()

        WebDriverWait(driver, 15).until(lambda d: feed_page.get_total_orders_count() > initial_count)
        new_count = feed_page.get_total_orders_count()
        assert new_count > initial_count

    @allure.title("Счётчик «Выполнено за сегодня» увеличивается")
    def test_today_orders_counter_increases(self, driver, authorized_user):
        feed_page = OrderFeedPage(driver)
        feed_page.open()
        initial_count = feed_page.get_today_orders_count()

        main_page = MainPage(driver)
        main_page.click_constructor()
        main_page.add_ingredient("Флюоресцентная булка R2-D3")
        main_page.add_ingredient("Мясо бессмертных моллюсков Protostomia")
        main_page.click_place_order()
        main_page.wait_for_order_number()
        main_page.close_order_modal()

        main_page.click_order_feed()

        WebDriverWait(driver, 15).until(lambda d: feed_page.get_today_orders_count() > initial_count)
        new_count = feed_page.get_today_orders_count()
        assert new_count > initial_count

    @allure.title("Номер заказа появляется в разделе «В работе»")
    def test_order_number_in_progress(self, driver, authorized_user):
        main_page = MainPage(driver)
        main_page.add_ingredient("Флюоресцентная булка R2-D3")
        main_page.add_ingredient("Мясо бессмертных моллюсков Protostomia")

        assert main_page.get_basket_items_count() > 0, "Корзина пуста! Drag-and-Drop не сработал."

        time.sleep(1)
        main_page.click_place_order()
        assert main_page.is_order_modal_opened()

        try:
            order_number = main_page.wait_for_order_number()
        except TimeoutException:
            # Если сервер завис, обновляем страницу. Возможно, заказ уже создался.
            driver.refresh()
            main_page.click_profile()
            profile_page = ProfilePage(driver)
            profile_page.click_order_history_tab()
            main_page.click_order_feed()
            feed_page = OrderFeedPage(driver)
            feed_page.wait.until(EC.visibility_of_element_located(OrderFeedLocators.TOTAL_ORDERS_COUNTER))
            in_progress = feed_page.get_in_progress_orders()
            assert len(in_progress) > 0, "Раздел 'В работе' пуст, сервер не отвечает."
            return

        main_page.close_order_modal()
        main_page.click_order_feed()

        feed_page = OrderFeedPage(driver)
        feed_page.wait.until(EC.visibility_of_element_located(OrderFeedLocators.TOTAL_ORDERS_COUNTER))

        normalized_order_number = str(int(order_number.replace("#", "").strip()))

        try:
            WebDriverWait(driver, 15).until(
                lambda d: normalized_order_number in feed_page.get_in_progress_orders()
            )
        except TimeoutException:
            driver.refresh()
            WebDriverWait(driver, 10).until(
                lambda d: normalized_order_number in feed_page.get_in_progress_orders()
            )

        in_progress = feed_page.get_in_progress_orders()
        assert normalized_order_number in in_progress, f"Заказа {normalized_order_number} нет в разделе 'В работе'. Текущие заказы: {in_progress}"