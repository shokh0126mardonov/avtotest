
from telegram import Update
from telegram.ext import ContextTypes
from handler.button import part_button

async def part_nav(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    try:
        _, page, part = query.data.split(":")
        page = int(page)
        part = int(part)
    except:
        return

    token = context.user_data.get("token")

    await query.edit_message_text(
        text="Sahifani tanlang:",
        reply_markup=part_button(part, token, page)
    )