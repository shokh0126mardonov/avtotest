from telegram import Update
from telegram.ext import ContextTypes


async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"""
    <b>👋 Assalomu alaykum, {update.effective_user.full_name}!</b>

    🌐 <b>Tilni tanlang:</b>

    🇺🇿 <b>O‘zbek tili</b> — /uz  
    🇷🇺 <b>Русский язык</b> — /ru  

    ━━━━━━━━━━━━━━━
    <i>Tilni tanlash uchun quyidagi tugmalardan foydalaning 👇</i>
    """,
        parse_mode="HTML"
    )


    # await update.message.reply_text("Username yuboring!")

