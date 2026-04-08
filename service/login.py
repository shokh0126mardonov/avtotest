import requests
from decouple import config

LOGIN_URL = config("BASE_URL") + "api/User/Login"


def check_user(username: str, password: str):
    response = requests.post(
        LOGIN_URL,
        json={
            "login": username,
            "password": password
        }
    )

    return response.status_code == 200