from telegram import Update
from telegram.ext import ContextTypes
import httpx
import asyncio
from urllib.parse import urljoin
from decouple import config


GET_TEST = config('BASE_URL') + "api/TestCase/GetAll"
BASE_URL = config('BASE_URL')


def escape_md(text: str) -> str:
    import re
    return re.sub(r'([_*[\]()~`>#+\-=|{}.!])', r'\\\1', str(text))


async def get_questions(token: str, lang: str, page_size: int):
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(
            url=GET_TEST,
            headers={"Authorization": f"Bearer {token}"},
            params={
                "language": lang,
                "pageSize": page_size,
                "isRandom": True,
            }
        )

        response.raise_for_status()
        data = response.json()
        return data.get("result", {})



def map_test_to_poll(item: dict) -> dict:
    question = item.get("question", "")[:300]

    options = []
    correct_index = None

    for i, ans in enumerate(item.get("testAnswers", [])):
        options.append(ans.get("answerText", "")[:100])

        if ans.get("isCorrect"):
            correct_index = i

    if correct_index is None:
        raise ValueError("Correct answer not found")

    media = item.get("mediaUrl")

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
    language = context.user_data.get('language')

    if not quiz:
        return

    questions = quiz["questions"]
    chat_id = quiz["chat_id"]

    while quiz["current_index"] < len(questions):
        item = questions[quiz["current_index"]]

        try:
            poll_data = map_test_to_poll(item)
            break  # valid savol topildi
        except Exception as e:
            print("⛔ SKIPPED:", e)

            quiz["total"] -= 1

            quiz["current_index"] += 1

    else:
        # savollar tugadi
        correct = quiz["correct_count"]
        total = quiz["total"]
        if language == 'uz':
            text = (
                f"📊 *Natija*\n\n"
                f"✅ To‘g‘ri: *{escape_md(correct)}*\n"
                f"❌ Noto‘g‘ri: *{escape_md(total - correct)}*\n"
                f"📈 Umumiy: *{escape_md(total)}*\n"
            )
        else:
            text = (
                f"📊 *Результат*\n\n"
                f"✅ Правильные: *{escape_md(correct)}*\n"
                f"❌ Неправильные: *{escape_md(total - correct)}*\n"
                f"📈 Всего: *{escape_md(total)}*\n"
            )
        
        if not text or not text.strip():
            text = "Natija mavjud emas"

        await context.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode="MarkdownV2"

        )

        context.user_data.pop("quiz", None)
        return

    # ===== shu joydan past = valid savol =====
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

    # eski task cancel
    task = quiz.get("task")
    if task and not task.done():
        task.cancel()

    quiz["task"] = asyncio.create_task(handle_timeout(context, 30))


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



async def handle_poll_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    answer = update.poll_answer
    poll_id = answer.poll_id
    selected_option = answer.option_ids[0] 
    quiz = context.user_data.get("quiz")
    if not quiz:
        return

    if poll_id != quiz.get("current_poll_id"):
        return

    index = quiz["current_index"]
    item = quiz["questions"][index]

    correct_index = None
    for i, ans in enumerate(item["testAnswers"]):
        if ans["isCorrect"]:
            correct_index = i
            break

    if selected_option == correct_index:
        quiz["correct_count"] += 1

    task = quiz.get("task")
    if task and not task.done():
        task.cancel()

    quiz["current_index"] += 1
    await send_next_question(context)

