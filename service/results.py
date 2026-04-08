import requests
from decouple import config
from pprint import pprint

RESULT_URl = config("BASE_URL") + 'api/Dashboard/GetExams'

def chech_result(token:str,user_id:str):
    data = requests.get(
        url=RESULT_URl,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "UserID":user_id
        }     
    )

    print(data.status_code)
    pprint(data.json())