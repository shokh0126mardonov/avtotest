from telegram.ext import Application,CommandHandler,ConversationHandler,MessageHandler,filters,CallbackQueryHandler,PollAnswerHandler
from decouple import config

from handler.command import start,language,user_result,test,logout
from handler.message import get_username,get_password,confirm_data,choice_number,random,part,send_part,part_nav
from service import handle_poll_answer

from utils import Lstate

def main() -> None:

    app = Application.builder().token(config("TOKEN")).build()
    app.add_handler(CommandHandler('start',start))
    app.add_handler(CommandHandler('natijalar',user_result))
    app.add_handler(CommandHandler("test",test))
    app.add_handler(CommandHandler('logout',logout))
    app.add_handler(CallbackQueryHandler(choice_number,pattern=r"^choice_(r|p)$"))
    app.add_handler(CallbackQueryHandler(random, pattern=r"^random_(20|50)$"))
    app.add_handler(CallbackQueryHandler(part, pattern=r"^part_(20|50)$"))
    app.add_handler(
        CallbackQueryHandler(send_part, pattern=r"^part_test:")
    )
    app.add_handler(
        CallbackQueryHandler(part_nav, pattern=r"^part_nav:")
    )

    app.add_handler(PollAnswerHandler(handle_poll_answer))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(['uz','ru'],language)],
        states={
            Lstate.username: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_username)
            ],
            Lstate.password: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_password)
            ],
            Lstate.confirm: [
                CallbackQueryHandler(confirm_data, pattern=r"^confirm_(true|false)$")
            ],
        },
        fallbacks=[]
    )

    app.add_handler(conv_handler)

    app.run_polling()


if __name__ == "__main__":
    main()