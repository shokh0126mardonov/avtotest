from telegram import InlineKeyboardButton,InlineKeyboardMarkup


def confirm(language:str):
    if language == "uz":
        keyboard = [
            [
                InlineKeyboardButton("✅ Tasdiqlash", callback_data="confirm_true"),
                InlineKeyboardButton("🔄 Qaytadan", callback_data="confirm_false"),
            ]
        ]

    elif language == "ru":
        keyboard = [
            [
                InlineKeyboardButton("✅ Подтвердить", callback_data="confirm_true"),
                InlineKeyboardButton("🔄 Заново", callback_data="confirm_false"),
            ]
        ]

    return InlineKeyboardMarkup(keyboard)