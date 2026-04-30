from telegram import Update
from telegram.ext import ContextTypes
import httpx
import asyncio
from urllib.parse import urljoin
from decouple import config
import random
from .check_token import check_status_by_token

GET_TEST = config('GET_TEST')
BASE_URL = config('BASE_URL')


def escape_md(text: str) -> str:
    import re
    return re.sub(r'([_*[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))


# =========================
# API CALL
# =========================
async def get_questions(
    token: str,
    lang: str,
    page_size: int,
    page: int | None = None,
    random: bool = False,
    refresh: str | None = None
):
    async with httpx.AsyncClient(timeout=10) as client:

        params = {
            "lang": lang,
            "page_size": page_size,
            "random": random,
        }

        if page is not None:
            params["page"] = page

        print("REQUEST PARAMS:", params)

        # 🔹 1. birinchi request
        response = await client.get(
            url=GET_TEST,
            headers={"Authorization": f"Bearer {token}"},
            params=params
        )

        # 🔹 2. agar token expired bo‘lsa
        if response.status_code == 401:

            if not refresh:
                return {"status": "login"}

            check = await check_status_by_token(refresh)

            if check["status_code"] == 200:
                token = check["access"]

                # 🔁 retry (client hali ochiq!)
                response = await client.get(
                    url=GET_TEST,
                    headers={"Authorization": f"Bearer {token}"},
                    params=params
                )
            else:
                return {"status": "login"}

        # 🔹 3. boshqa xatolar
        response.raise_for_status()

        data = response.json()

        # 🔹 4. normalize
        if isinstance(data, list):
            return {"items": data}

        return {"items": data.get("results", [])}



def map_test_to_poll(item: dict) -> dict:
    question = item.get("question", "")[:300]

    answers = item.get("answers", [])

    if not answers:
        raise ValueError("No answers")

    # 🔥 SHUFFLE
    random.shuffle(answers)

    options = []
    correct_index = None

    for i, ans in enumerate(answers):
        options.append(ans.get("answer_text_uz", "")[:100])

        if ans.get("is_correct"):
            correct_index = i

    if correct_index is None:
        raise ValueError("Correct answer not found")

    media = item.get("media")

    if media and not media.startswith("http"):
        media = urljoin(BASE_URL, media)

    return {
        "question": question,
        "options": options[:10],
        "correct_index": correct_index,
        "explanation": (item.get("explanation") or "")[:200],
        "media": media
    }


async def send_next_question(context: ContextTypes.DEFAULT_TYPE):
    quiz = context.user_data.get("quiz")

    if not quiz:
        return

    questions = quiz["questions"]
    chat_id = quiz["chat_id"]

    while quiz["current_index"] < len(questions):
        item = questions[quiz["current_index"]]

        try:
            poll_data = map_test_to_poll(item)
            break
        except Exception:
            quiz["total"] -= 1
            quiz["current_index"] += 1

    else:
        correct = quiz["correct_count"]
        total = quiz["total"]

        text = (
            f"📊 Natija\n\n"
            f"✅ To‘g‘ri: {correct}\n"
            f"❌ Noto‘g‘ri: {total - correct}\n"
            f"📈 Umumiy: {total}"
        )

        await context.bot.send_message(chat_id=chat_id, text=text)
        context.user_data.pop("quiz", None)
        return

    if poll_data["media"]:
        try:
            await context.bot.send_photo(chat_id, poll_data["media"])
        except Exception:
            pass

    message = await context.bot.send_poll(
        chat_id=chat_id,
        question=poll_data["question"],
        options=poll_data["options"],
        type="quiz",
        correct_option_id=poll_data["correct_index"],
        explanation=poll_data["explanation"],
        open_period=30,
        is_anonymous=False
    )

    quiz["current_poll_id"] = message.poll.id

    task = quiz.get("task")
    if task and not task.done():
        task.cancel()

    quiz["task"] = asyncio.create_task(handle_timeout(context, 30))


# =========================
# TIMEOUT
# =========================
async def handle_timeout(context: ContextTypes.DEFAULT_TYPE, delay: int):
    try:
        await asyncio.sleep(delay)

        quiz = context.user_data.get("quiz")
        if not quiz:
            return

        quiz["current_index"] += 1
        await send_next_question(context)

    except asyncio.CancelledError:
        pass


# =========================
# ANSWER HANDLER
# =========================
async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer

    if not answer.option_ids:
        return

    selected_option = answer.option_ids[0]
    poll_id = answer.poll_id

    quiz = context.user_data.get("quiz")
    if not quiz:
        return

    if poll_id != quiz.get("current_poll_id"):
        return

    index = quiz["current_index"]
    questions = quiz.get("questions", [])

    if index >= len(questions):
        return

    item = questions[index]

    answers = item.get("answers")
    if not answers:
        quiz["current_index"] += 1
        await send_next_question(context)
        return

    correct_index = None
    for i, ans in enumerate(answers):
        if ans.get("is_correct"):
            correct_index = i
            break

    if correct_index is None:
        quiz["current_index"] += 1
        await send_next_question(context)
        return

    if selected_option == correct_index:
        quiz["correct_count"] += 1

    task = quiz.get("task")
    if task and not task.done():
        task.cancel()

    quiz["current_index"] += 1
    await send_next_question(context)