from telegram import Update
from telegram.ext import ContextTypes
from decouple import config
import httpx

from handler.button import part_button
from service import check_status_by_token


GET_TEST = config('GET_TEST')

async def part(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    try:
        await query.answer()
    except:
        pass

    token = context.user_data.get("token")
    refresh = context.user_data.get("refresh")

    part_size = int(query.data.split("_")[1])

    async with httpx.AsyncClient() as client:

        response = await client.get(
            url=GET_TEST,
            headers={"Authorization": f"Bearer {token}"}
        )

        if response.status_code == 401:
            check = await check_status_by_token(refresh)

            if check["status_code"] == 200:
                token = check["access"]
                context.user_data["token"] = token

                response = await client.get(
                    url=GET_TEST,
                    headers={"Authorization": f"Bearer {token}"}
                )
            else:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="Qaytadan login qiling!"
                )
                return

        data = response.json()
        count = data.get("count", 0)

    # 🔑 COUNT NI BERAMIZ
    keyboard = part_button(part_size, count, page=1)

    await query.edit_message_text(
        text=f"{part_size} talik test tanlandi",
        reply_markup=keyboard
    )