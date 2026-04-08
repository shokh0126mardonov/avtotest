from telegram import Update
from telegram.ext import ContextTypes


async def user_result(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        if context.user_data['login']:
            await update.message.reply_text("mana sizni natijangiz")
    except:
        await update.message.reply_text("Natijalarizni ko'rish uchun oldin /start buyrug'ini bosib login qiling")