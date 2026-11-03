import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class MainPage(BasePage):
    def open(self):
        super().open(BASE_URL)

    def click_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_BUTTON)

    def click_order_feed(self):
        self.click(MainPageLocators.ORDER_FEED_BUTTON)

    def click_profile(self):
        self.click(MainPageLocators.PROFILE_BUTTON)

    def click_ingredient(self, name):
        self.click(MainPageLocators.INGREDIENT_IMAGE(name))

    def add_ingredient(self, name):
        """Перетаскивает ингредиент в корзину. Для Firefox использует JS-события."""
        source = self.find_element(MainPageLocators.INGREDIENT_IMAGE(name))
        target = self.find_element(
            (By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list')] | //div[contains(@class, 'BurgerConstructor_basket')]")
        )
        
        if self.driver.name.lower() == 'firefox':
            # JS-эмуляция Drag-and-Drop для Firefox
            self.driver.execute_script("""
                function simulateDragDrop(sourceNode, destinationNode) {
                    var EVENT_TYPES = { DRAG_END: 'dragend', DRAG_START: 'dragstart', DROP: 'drop' };
                    function createCustomEvent(type) {
                        var event = new CustomEvent("CustomEvent");
                        event.initCustomEvent(type, true, true, null);
                        event.dataTransfer = {
                            data: {},
                            setData: function(type, val) { this.data[type] = val; },
                            getData: function(type) { return this.data[type]; }
                        };
                        return event;
                    }
                    function dispatchEvent(node, type, event) {
                        if (node.dispatchEvent) { return node.dispatchEvent(event); }
                        if (node.fireEvent) { return node.fireEvent("on" + type, event); }
                    }
                    var event = createCustomEvent(EVENT_TYPES.DRAG_START);
                    dispatchEvent(sourceNode, EVENT_TYPES.DRAG_START, event);
                    var dropEvent = createCustomEvent(EVENT_TYPES.DROP);
                    dropEvent.dataTransfer = event.dataTransfer;
                    dispatchEvent(destinationNode, EVENT_TYPES.DROP, dropEvent);
                    var dragEndEvent = createCustomEvent(EVENT_TYPES.DRAG_END);
                    dragEndEvent.dataTransfer = event.dataTransfer;
                    dispatchEvent(sourceNode, EVENT_TYPES.DRAG_END, dragEndEvent);
                }
                simulateDragDrop(arguments[0], arguments[1]);
            """, source, target)
        else:
            # Стандартный Drag-and-Drop для Chrome
            ActionChains(self.driver).drag_and_drop(source, target).perform()
            
        time.sleep(0.5)  # Даем React время обновить корзину

    def get_basket_items_count(self):
        """Возвращает количество ингредиентов в корзине."""
        elements = self.driver.find_elements(By.XPATH, "//ul[contains(@class, 'BurgerConstructor_basket__list')]/li")
        return len(elements)

    def get_ingredient_counter(self, name):
        text = self.get_text(MainPageLocators.INGREDIENT_COUNTER(name))
        return int(text) if text.strip().isdigit() else 0

    def is_ingredient_modal_opened(self):
        return self.is_element_visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def close_ingredient_modal(self):
        element = self.find_element(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)

    def is_ingredient_modal_closed(self):
        try:
            self.wait.until(EC.invisibility_of_element_located(MainPageLocators.INGREDIENT_MODAL_TITLE))
            return True
        except Exception:
            return False

    def click_place_order(self):
        element = self.find_element(MainPageLocators.PLACE_ORDER_BUTTON)
        self.driver.execute_script("arguments[0].click();", element)

    def is_order_modal_opened(self):
        return self.is_element_visible(MainPageLocators.ORDER_NUMBER_MODAL)

    def get_order_number(self):
        return self.get_text(MainPageLocators.ORDER_NUMBER_MODAL)

    def wait_for_order_number(self):
        """Смена номера заказа"""
        WebDriverWait(self.driver, 30).until(lambda d: self.get_order_number() != "9999")
        return self.get_order_number()

    def close_order_modal(self):
        self.driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
        self.wait.until(EC.invisibility_of_element_located(MainPageLocators.ORDER_NUMBER_MODAL))