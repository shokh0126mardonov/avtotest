from telegram.ext import Application,CommandHandler,ConversationHandler,MessageHandler,filters,CallbackQueryHandler
from decouple import config

from handler.command import start,language
from handler.message import get_username,get_password,confirm_data

from utils import Lstate

def main() -> None:

    app = Application.builder().token(config("TOKEN")).build()
    app.add_handler(CommandHandler('start',start))

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