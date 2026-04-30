from decouple import config
import httpx

REFRESH_URL = config("REFRESH_URL")

async def check_status_by_token(refresh: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=REFRESH_URL,
            json={"refresh": refresh}
        )

    if response.status_code == 200:
        return {
            "status_code": 200,
            "access": response.json().get("access")
        }

    if response.status_code == 401:
        return {
            "status_code": 401
        }

    return {
        "status_code": response.status_code
    }