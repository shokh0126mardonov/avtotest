from telegram import Update
from telegram.ext import ContextTypes

from handler.button import test_choice_buttons

async def test(update:Update,context:ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id',False)
    language = context.user_data.get("language",False) 

    if user_id:
        if language == 'uz':
            text = "Tanlang"
        elif language == 'ru':
            text = 'Выбирать'
        await update.message.reply_text(
            text,
            reply_markup=test_choice_buttons(language)
        )
    else:
        await update.message.reply_text(
            text = (
            "⚠️ *Foydalanuvchi topilmadi*\n\n"
            "Siz hali tizimga kirmagansiz.\n\n"
            "👉 Davom etish uchun quyidagini bosing:\n"
            "/start"
            )
        )

