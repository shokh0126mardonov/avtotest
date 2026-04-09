from telegram import Update
from telegram.ext import ContextTypes


async def random(update:Update,context:ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get('language')
    user_id = context.user_data.get('user_id')

    query = update.callback_query
    await query.answer()

    if user_id:


        await query.edit_message_text("Mana test")
    else:
        await query.edit_message_text(            text = (
            "⚠️ *Foydalanuvchi topilmadi*\n\n"
            "Siz hali tizimga kirmagansiz.\n\n"
            "👉 Davom etish uchun quyidagini bosing:\n"
            "/start"
            ))