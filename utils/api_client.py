import requests

BASE_URL = "https://qa-stellarburgers.education-services.ru"


class ApiClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {"Content-Type": "application/json"}

    def set_token(self, token):
        self.headers["Authorization"] = token

    def register_user(self, email, password, name):
        payload = {"email": email, "password": password, "name": name}
        return requests.post(f"{self.base_url}/api/auth/register", json=payload)

    def delete_user(self):
        return requests.delete(
            f"{self.base_url}/api/auth/user", headers=self.headers
        )