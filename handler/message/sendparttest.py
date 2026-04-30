from telegram import Update
from telegram.ext import ContextTypes
from service import get_questions,send_next_question

async def send_part(update: Update, context: ContextTypes.DEFAULT_TYPE):
    language = context.user_data.get('language')
    token = context.user_data.get('token')
    user_id = context.user_data.get('user_id')

    query = update.callback_query
    await query.answer()

    if not user_id or not token:
        await query.edit_message_text(
            text=(
                "⚠️ *Foydalanuvchi topilmadi*\n\n"
                "Siz hali tizimga kirmagansiz.\n\n"
                "👉 /start"
            ),
            parse_mode="Markdown"
        )
        return

    # 🔹 YANGI FORMAT: part_test:{page}:{part}
    try:
        _, page_number, part = query.data.split(":")
        page_number = int(page_number)
        page_size = int(part)
    except (ValueError, IndexError):
        await query.answer("Noto‘g‘ri data", show_alert=True)
        return

    # 🔹 state sync (agar kerak bo‘lsa)
    context.user_data['page_size'] = page_size

    try:
        data = await get_questions(
            token=token,
            lang=language,
            page_size=page_size,
            page=page_number,
            random=False
        )

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
            "total": len(items)
        }

        start_text = (
            "🚀 Test boshlandi"
            if language == "uz"
            else "🚀 Тест начался"
        )

        await query.edit_message_text(start_text)

        await send_next_question(context)

    except Exception as e:
        await query.edit_message_text(f"❌ Xatolik: {str(e)}")