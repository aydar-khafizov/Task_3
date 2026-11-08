from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from config import BASE_URL
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    def open(self):
        super().open(BASE_URL)

    def click_constructor(self):
        self.click(MainPageLocators.CONSTRUCTOR_BUTTON)

    def click_order_feed(self):
        self.click(MainPageLocators.ORDER_FEED_BUTTON)

    def click_profile(self):
        self.click(MainPageLocators.PROFILE_BUTTON)

    def is_constructor_opened(self):
        url = self.get_current_url()
        return url.endswith("/") and "qa-stellarburgers" in url

    def is_order_feed_opened(self):
        return "/feed" in self.get_current_url()

    def click_ingredient(self, name):
        self.click(MainPageLocators.INGREDIENT_IMAGE(name))

    def get_ingredient_counter(self, name):
        try:
            text = self.get_text(MainPageLocators.INGREDIENT_COUNTER(name))
            return int(text) if text.strip().isdigit() else 0
        except Exception:
            return 0

    def add_ingredient(self, name):
        initial_counter = self.get_ingredient_counter(name)

        source = self.find_element(MainPageLocators.INGREDIENT_IMAGE(name))
        target = self.find_element(MainPageLocators.BASKET_LIST)

        if self.driver.name.lower() == "firefox":
            self.execute_script("""
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
            ActionChains(self.driver).drag_and_drop(source, target).perform()

        self.wait_until(lambda d: self.get_ingredient_counter(name) > initial_counter)

    def get_basket_items_count(self):
        return len(self.find_elements(MainPageLocators.BASKET_ITEMS))

    def is_ingredient_modal_opened(self):
        return self.is_element_visible(MainPageLocators.INGREDIENT_MODAL_TITLE)

    def close_ingredient_modal(self):
        element = self.find_element(MainPageLocators.MODAL_CLOSE_BUTTON)
        self.execute_script("arguments[0].click();", element)

    def is_ingredient_modal_closed(self):
        try:
            self.wait_until_invisible(MainPageLocators.INGREDIENT_MODAL_TITLE, timeout=10)
            return True
        except Exception:
            return False

    def click_place_order(self):
        element = self.find_element(MainPageLocators.PLACE_ORDER_BUTTON)
        self.execute_script("arguments[0].click();", element)

    def is_order_modal_opened(self):
        return self.is_element_visible(MainPageLocators.ORDER_NUMBER_MODAL)

    def get_order_number(self):
        return self.get_text(MainPageLocators.ORDER_NUMBER_MODAL)

    def wait_for_order_number(self):
        # Используем универсальный метод wait_until
        self.wait_until(lambda d: self.get_order_number() != "9999", timeout=60)
        return self.get_order_number()

    def close_order_modal(self):
        body = self.find_element(MainPageLocators.BODY)
        body.send_keys(Keys.ESCAPE)
        self.wait_until_invisible(MainPageLocators.ORDER_NUMBER_MODAL)