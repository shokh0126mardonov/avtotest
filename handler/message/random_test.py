from telegram import Update
from telegram.ext import ContextTypes

from service import get_questions,send_next_question

async def random(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get('language')
    token = context.user_data.get('token')
    user_id = context.user_data.get('user_id')

    query = update.callback_query
    await query.answer()

    try:
        page_size = int(query.data.split('_')[1])
    except Exception:
        page_size = 5

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

    try:
        data = await get_questions(token, language, page_size)
        items = data.get("items", [])

        if not items:
            await query.edit_message_text("❌ Savollar topilmadi")
            return

        context.user_data["quiz"] = {
            "questions": items,
            "current_index": 0,
            "task": None,
            "chat_id": update.effective_chat.id,
            "current_poll_id": None,
            "correct_count": 0,
            "total": len(items)  # keyin kamayadi
        }

        if language == 'uz':
            await query.edit_message_text("🚀 Test boshlandi")
        elif language == 'ru':
            await query.edit_message_text("🚀 Тест начался")

        await send_next_question(context)

    except Exception as e:
        await query.edit_message_text(f"❌ Xatolik: {str(e)}")