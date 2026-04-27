from telegram import Update
from telegram.ext import ContextTypes


async def part(update:Update,context:ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get('language')
    token = context.user_data.get('token')
    user_id = context.user_data.get('user_id')


    query = update.callback_query
    await query.answer()

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
    
    data = query.data.split('_')[1]

    await query.edit_message_text(
        f"siz part {data} ni tanladingiz!"
    )