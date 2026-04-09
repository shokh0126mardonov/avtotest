from telegram import Update
from telegram.ext import ContextTypes,ConversationHandler
from pprint import pprint


from utils import Lstate
from ..button import confirm
from service import check_user



async def get_username(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data['username'] = update.message.text.strip()
    language = context.user_data['language']


    if language == 'uz':
        await update.message.reply_text(
            """
    <b>🔐 Parol</b>

    🔑 Password yuboring:
    """,
            parse_mode="HTML"
        )
        return Lstate.password

    elif language == "ru":
        await update.message.reply_text(
            """
    <b>🔐 Пароль</b>

    🔑 Отправьте пароль:
    """,
            parse_mode="HTML"
        )
        return Lstate.password


async def get_password(update:Update,context:ContextTypes.DEFAULT_TYPE):
    context.user_data['password'] = update.message.text.strip()
    language = context.user_data['language']

    reply_markup = confirm(language)

    if language == 'uz':
        await update.message.reply_text(
        f"""
            <b>📋 Ma’lumotlaringizni tasdiqlang</b>

            👤 <b>Username:</b> <code>{context.user_data['username']}</code>  
            🔐 <b>Password:</b> <code>{context.user_data['password']}</code>

            ━━━━━━━━━━━━━━━
            <i>Hammasi to‘g‘rimi?</i>
        """,
            parse_mode="HTML",
            reply_markup = reply_markup
            )
        return Lstate.confirm

    elif language == "ru":
        await update.message.reply_text(
        f"""
            <b>📋 Подтвердите ваши данные</b>

            👤 <b>Имя пользователя:</b> <code>{context.user_data['username']}</code>  
            🔐 <b>Пароль:</b> <code>{context.user_data['password']}</code>

            ━━━━━━━━━━━━━━━
            <i>Все верно?</i>
        """,
            parse_mode="HTML",
            reply_markup = reply_markup

        )
        return Lstate.confirm
    
async def confirm_data(update:Update,context:ContextTypes.DEFAULT_TYPE):
    language = context.user_data['language']
    query = update.callback_query
    await query.answer()

    if language == 'uz':

        if query.data == "confirm_true":

            user_data =  check_user(context.user_data.get("username"),context.user_data.get("password"))

            if user_data.get("status_code"):
                context.user_data['language'] = language
                context.user_data['user_id'] = user_data.get('user_id')
                context.user_data['token'] = user_data.get('token')


                await query.edit_message_text("tasdiqlandi")
                return ConversationHandler.END
            
            await query.edit_message_text("malumotlariz topilmadi")                
            return ConversationHandler.END


        
        elif query.data == "confirm_false":
            await query.edit_message_text("👤 username yuboring")
            return Lstate.username
        
    elif language == 'ru':

        if query.data == "confirm_true":
            user_data =  check_user(context.user_data.get("username"),context.user_data.get("password"))

            if user_data.get("status_code"):

                context.user_data['language'] = language
                context.user_data['user_id'] = user_data.get('user_id')
                context.user_data['token'] = user_data.get('token')
                
                await query.edit_message_text("подтвержденный")
                return ConversationHandler.END
            
            await query.edit_message_text("Ваши данные не найдены.")
            return ConversationHandler.END


        elif query.data == "confirm_false":
            await query.edit_message_text("👤 Отправьте username:")

            return Lstate.username