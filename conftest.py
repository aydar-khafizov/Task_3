import os

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from pages.login_page import LoginPage
from utils.api_client import ApiClient
from utils.data_generator import generate_random_email, generate_random_string

HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"


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
    email = generate_random_email()
    password = generate_random_string()
    name = generate_random_string()

    response = api_client.register_user(email, password, name)
    
    
    if response.status_code != 200:
        pytest.fail(f"Не удалось создать пользователя в фикстуре. Ошибка API: {response.text}")
        
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
    login_page = LoginPage(driver)
    login_page.open()
    login_page.login(registered_user["email"], registered_user["password"])
    login_page.wait_until_url_not_contains("/login")
    return registered_user