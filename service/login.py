import requests
from decouple import config
from pprint import pprint

LOGIN_URL = config("BASE_URL") + "api/User/Login"


def check_user(username: str, password: str):
    response = requests.post(
        LOGIN_URL,
        json={
            "login": username,
            "password": password
        }
    )
    result = response.json().get("result")

    return {
       "status_code" : response.status_code == 200,
       "token":  result.get("accessToken"),
       "user_id":result.get("user").get("id")
        }