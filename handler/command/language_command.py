from telegram import Update
from telegram.ext import ContextTypes

from utils import Lstate

async def language(update:Update,context:ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace('/','')

    context.user_data['language'] = text

    if text == 'uz':
        await update.message.reply_text(
        f"""<b>🔐 Tasdiqlash</b>
        👤 Username yuboring:
        """,
        parse_mode="HTML"
        )

    elif text == 'ru':
        await update.message.reply_text(
            f"""
                <b>🔐 Подтверждение</b>
                👤 Отправьте username:
                """,
            parse_mode="HTML"
        )

    return Lstate.username
    