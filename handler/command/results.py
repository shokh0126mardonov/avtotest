from telegram import Update
from telegram.ext import ContextTypes
from service import chech_result

async def user_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = context.user_data.get('user_id',False)
    language = context.user_data.get("language",False) 
    token = context.user_data.get("token",False)
    user_id = context.user_data.get("user_id",None)

    
  
    if user_id:
        # chech_result(token,user_id)
        if language == 'uz':
            text = (
                "📊 *Sizning natijalaringiz*\n\n"
                "━━━━━━━━━━━━━━━\n"
                "✅ Testlar: *12 ta*\n"
                "🏆 To‘g‘ri javoblar: *10 ta*\n"
                "❌ Xatolar: *2 ta*\n"
                "📈 Natija: *83%*\n"
                "━━━━━━━━━━━━━━━\n\n"
                "💡 Yaxshi natija! Davom eting 🚀"
            )

            await update.message.reply_text(text, parse_mode="Markdown")
        elif language == 'ru':
            text = (
                "📊 *Ваши результаты*\n\n"
                "━━━━━━━━━━━━━━━\n"
                "📚 Тесты: *12*\n"
                "🏆 Правильные ответы: *10*\n"
                "❌ Ошибки: *2*\n"
                "📈 Результат: *83%*\n"
                "━━━━━━━━━━━━━━━\n\n"
                "💡 Отличный результат! Продолжайте 🚀"
            )
            await update.message.reply_text(text, parse_mode="Markdown")
    else:
        text = (
            "⚠️ *Foydalanuvchi topilmadi*\n\n"
            "Siz hali tizimga kirmagansiz.\n\n"
            "👉 Davom etish uchun quyidagini bosing:\n"
            "/start"
        )

        await update.message.reply_text(text, parse_mode="Markdown")