import os
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.api_client import ApiClient
from utils.data_generator import generate_random_email, generate_random_string

HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
BASE_URL = "https://qa-stellarburgers.education-services.ru"


def get_driver(browser_name: str):
    if browser_name == "chrome":
        options = ChromeOptions()
        if HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        return webdriver.Chrome(options=options)
    if browser_name == "firefox":
        options = FirefoxOptions()
        if HEADLESS:
            options.add_argument("-headless")
        return webdriver.Firefox(options=options)
    raise ValueError(f"Unsupported browser: {browser_name}")


@pytest.fixture(params=["chrome", "firefox"], ids=["chrome", "firefox"])
def driver(request):
    browser = get_driver(request.param)
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.fixture
def api_client():
    return ApiClient()


@pytest.fixture
def registered_user(api_client):
    """Создаёт уникального пользователя через API и удаляет его после теста."""
    email = generate_random_email()
    password = generate_random_string()
    name = generate_random_string()

    response = api_client.register_user(email, password, name)
    assert response.status_code == 200, f"Ошибка API: {response.text}"
    data = response.json()

    yield {
        "email": email,
        "password": password,
        "name": name,
        "token": data["accessToken"],
        "refresh_token": data["refreshToken"],
    }

    cleanup = ApiClient()
    cleanup.set_token(data["accessToken"])
    cleanup.delete_user()


@pytest.fixture
def authorized_user(driver, registered_user):
    """Логинит созданного через API пользователя через UI."""
    driver.get(f"{BASE_URL}/login")

    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, "//input[@name='name']"))
    )

    driver.find_element(By.XPATH, "//input[@name='name']").send_keys(registered_user["email"])
    driver.find_element(By.XPATH, "//input[@name='Пароль']").send_keys(registered_user["password"])

    time.sleep(1) # Даем React время

    driver.find_element(By.XPATH, "//button[text()='Войти']").click()

    # Ждем появления токена
    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return window.localStorage.getItem('accessToken');") is not None
    )
    
    return registered_user