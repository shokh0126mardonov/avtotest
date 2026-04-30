from telegram import InlineKeyboardMarkup, InlineKeyboardButton
import math
from decouple import config

GET_TEST = config('GET_TEST')


def part_button(
        part: int, 
        count:int,
        page: int = 1
        ):
 

    total_pages = math.ceil(count / part)

    window_size = 8  # 4x2
    total_windows = math.ceil(total_pages / window_size)

    # current window bounds
    start = (page - 1) * window_size + 1
    end = min(start + window_size - 1, total_pages)

    buttons = []

    # 🔹 4x2 grid
    row = []
    for idx, i in enumerate(range(start, end + 1), 1):
        row.append(
            InlineKeyboardButton(
                text=str(i),
                callback_data=f"part_test:{i}:{part}"
            )
        )

        if idx % 4 == 0:
            buttons.append(row)
            row = []

    if row:
        buttons.append(row)

    # 🔹 navigation
    nav = []

    if page > 1:
        nav.append(
            InlineKeyboardButton(
                "⬅️",
                callback_data=f"part_nav:{page-1}:{part}"
            )
        )

    nav.append(
        InlineKeyboardButton(
            f"{page}/{total_windows}",
            callback_data="noop"
        )
    )

    if page < total_windows:
        nav.append(
            InlineKeyboardButton(
                "➡️",
                callback_data=f"part_nav:{page+1}:{part}"
            )
        )

    buttons.append(nav)

    return InlineKeyboardMarkup(buttons)