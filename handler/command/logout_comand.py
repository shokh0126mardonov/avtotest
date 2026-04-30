from telegram import Update
from telegram.ext import ContextTypes
from decouple import config
import requests

LOGOUT_URL = config("LOGOUT_URL")

async def logout(update:Update,context:ContextTypes.DEFAULT_TYPE):
    id = update.effective_user.id

    request = requests.post(
        url=LOGOUT_URL,
        json={
            "telegram_id":id
        }
    )
    print(request.status_code)
    if request.status_code == 204:
        await update.message.reply_text(
            "siz logout qilindingiz!"
        )
    else:
        await update.message.reply_text("Siz tizimda mavjud emassiz!")