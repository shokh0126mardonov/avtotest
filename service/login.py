import requests
from decouple import config

LOGIN_URL = config("LOGIN_URL") 


def check_user(username: str, password: str,chat_id:int):
    response = requests.post(
        LOGIN_URL,
        json={
            "username": username,
            "password": password,
            "telegram_id":chat_id
        }
    )   

    result = response.json()
    if response.status_code == 200:
        return {
        "status_code" : 200,
        "token":  result.get("access"),
        "user_id":result.get("id")
            }
    return {
        "status_code":403
    }