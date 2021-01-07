"""Telegram version of a support bot."""
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from env_settings import env_settings
from questions import get_random_question
from redis_adapter import redis_adapter


NEW_QUESTION = 'Новый вопрос'
GIVE_UP = 'Сдаться'
SCORE = 'Мой счёт'


def echo_handler(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    custom_keyboard = [[NEW_QUESTION, GIVE_UP], [SCORE]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    message = update.message.text
    if message == NEW_QUESTION:
        question, answer = get_random_question()
        update.message.reply_text(question, reply_markup=reply_markup)
    else:
        update.message.reply_text(update.message.text, reply_markup=reply_markup)


def start_bot() -> None:
    """Start Telegram bot."""
    bot_token = env_settings.tg_bot_token
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo_handler, pass_user_data=True))

    updater.start_polling()
    updater.idle()
