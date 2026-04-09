from telegram import InlineKeyboardButton,InlineKeyboardMarkup


def test_choice_buttons(lang:str):
    if lang == 'uz':
        buttons = [
            [
                InlineKeyboardButton(text="🎲 Random", callback_data='choice_r'),
                InlineKeyboardButton(text="📂 Partlar", callback_data='choice_p')
            ]
        ]

    elif lang == 'ru':
        buttons = [
            [
                InlineKeyboardButton(text="🎲 Случайно", callback_data='choice_r'),
                InlineKeyboardButton(text="📂 Разделы", callback_data='choice_p')
            ]
        ]
    return InlineKeyboardMarkup(buttons)


def number_choice(data:str):
    if data == 'choice_r':
            buttons = [
                [
                    InlineKeyboardButton(text="20", callback_data='random_20'),
                    InlineKeyboardButton(text="50", callback_data='random_50')
                ]
            ]
    elif data == 'choice_p':
            buttons = [
                [
                    InlineKeyboardButton(text="20", callback_data='part_20'),
                    InlineKeyboardButton(text="50", callback_data='part_50')
                ]
            ]
    return InlineKeyboardMarkup(buttons)