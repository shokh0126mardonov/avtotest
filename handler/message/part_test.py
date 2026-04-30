from telegram import Update
from telegram.ext import ContextTypes
from handler.button import part_button



async def part(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get('language')
    token = context.user_data.get('token')
    user_id = context.user_data.get('user_id')

    query = update.callback_query

    try:
        await query.answer()
    except Exception:
        pass

    if not user_id:
        await query.edit_message_text(
            text=(
                "⚠️ *Foydalanuvchi topilmadi*\n\n"
                "Siz hali tizimga kirmagansiz.\n\n"
                "👉 /start"
            ),
            parse_mode="Markdown"
        )
        return

    # 🔑 SAFE PARSE (bu ham crash bo‘lishi mumkin edi)
    try:
        page_size = int(query.data.split('_')[1])
    except (IndexError, ValueError):
        page_size = 20  # fallback

    context.user_data['page_size'] = page_size

    await query.edit_message_text(
        text=f"siz part {page_size} ni tanladingiz!",
        reply_markup=part_button(page_size, token, page=1)
    )