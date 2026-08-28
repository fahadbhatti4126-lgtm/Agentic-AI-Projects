import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from langchain_groq import ChatGroq


load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    api_key=GROQ_API_KEY,
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Assalam-o-Alaikum!\n\n"
        "I am the University of Layyah AI Assistant.\n"
        "Send me a question and I will try to help you."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_message = update.message.text

    try:
        response = llm.invoke(user_message)

        await update.message.reply_text(response.content)

    except Exception as e:

        await update.message.reply_text(
            f"Sorry, an error occurred:\n{e}"
        )


def main():

    if not TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is missing from .env")

    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing from .env")

    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("🤖 Telegram AI Assistant is running...")

    app.run_polling()


if __name__ == "__main__":
    main()