from telegram import Update
from telegram.ext import ContextTypes

from ..button import number_choice

async def choice_number(update:Update,context:ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data

    language = context.user_data.get("language")

    if language == 'uz':
        await query.edit_message_text("Tanlang",reply_markup=number_choice(data))
    elif language == 'ru':
        await query.edit_message_text("Выбирать",reply_markup=number_choice(data))
