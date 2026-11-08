from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self, url):
        self.driver.get(url)

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def click(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        try:
            element.click()
        except ElementClickInterceptedException:
            self.execute_script("arguments[0].click();", element)

    def click_js(self, locator):
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.execute_script("arguments[0].click();", element)

    def send_keys(self, locator, text):
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        return self.find_element(locator).text

    def is_element_visible(self, locator, timeout=5):
        try:
            self.wait_until(EC.visibility_of_element_located(locator), timeout)
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator):
        try:
            self.wait_until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False

    # --- Универсальные ожидания ---
    def wait_until(self, condition, timeout=15):
        """Универсальный метод для ожидания любого условия."""
        return WebDriverWait(self.driver, timeout).until(condition)

    def wait_until_invisible(self, locator, timeout=15):
        self.wait_until(EC.invisibility_of_element_located(locator), timeout)

    def wait_until_visible(self, locator, timeout=15):
        self.wait_until(EC.visibility_of_element_located(locator), timeout)

    def wait_until_url_contains(self, url_part, timeout=15):
        self.wait_until(EC.url_contains(url_part), timeout)

    def wait_until_url_not_contains(self, url_part, timeout=15):
        self.wait_until(lambda d: url_part not in d.current_url, timeout)

    def wait_until_page_contains(self, text, timeout=15):
        self.wait_until(lambda d: text in d.page_source, timeout)

    def execute_script(self, script, *args):
        return self.driver.execute_script(script, *args)

    def get_current_url(self):
        return self.driver.current_url

    def refresh_page(self):
        self.driver.refresh()

    def get_page_source(self):
        return self.driver.page_source

    def is_page_contains_text(self, text):
        return text in self.driver.page_source

    def is_url_contains(self, url_part):
        return url_part in self.driver.current_url