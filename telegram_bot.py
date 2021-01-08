"""Telegram version of a support bot."""
from enum import Enum

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext, ConversationHandler, RegexHandler)
from redis import Redis

from env_settings import env_settings
from questions import get_random_question, get_answer, is_correct_answer


NEW_QUESTION_TEXT = 'Новый вопрос'
GIVE_UP_TEXT = 'Сдаться'
SCORE_TEXT = 'Мой счёт'

BOT_DATA_REDIS_DB = 'redis_db'

menu_buttons = [[NEW_QUESTION_TEXT, GIVE_UP_TEXT], [SCORE_TEXT]]
reply_markup = ReplyKeyboardMarkup(menu_buttons)


class BotState(Enum):
    MENU = 'Choice'
    QUESTION = 'Question'


def handle_start(update: Update, context: CallbackContext):
    """TODO"""
    update.message.reply_text(
        f'Добрый день! Нажмите "{NEW_QUESTION_TEXT}" для начала игры.',
        reply_markup=reply_markup
    )

    return BotState.MENU


def handle_new_question_request(
        update: Update,
        context: CallbackContext
):
    """TODO"""
    redis_db = context.bot_data[BOT_DATA_REDIS_DB]
    question = get_random_question()
    redis_db.set(update.effective_user.id, question)
    update.message.reply_text(question)

    return BotState.QUESTION


def handle_solution_attempt(
        update: Update,
        context: CallbackContext
):
    """TODO"""
    redis_db = context.bot_data[BOT_DATA_REDIS_DB]
    question = redis_db.get(update.effective_user.id).decode('utf-8')
    answer = get_answer(question)
    if is_correct_answer(update.message.text, answer):
        reply_text = 'Поздравляем! Ответ верен. Ещё разок?'
    else:
        reply_text = f'Неправильно :( Правильный ответ - "{answer}". Хотите попробовать ещё раз?'
    update.message.reply_text(reply_text)

    return BotState.MENU


def handle_give_up_request(
        update: Update,
        context: CallbackContext
):
    """TODO"""
    redis_db = context.bot_data[BOT_DATA_REDIS_DB]
    question = redis_db.get(update.effective_user.id).decode('utf-8')
    answer = get_answer(question)
    update.message.reply_text(f'Правильный ответ: "{answer}". Хотите попробовать ещё раз?')

    return BotState.MENU


def start_bot() -> None:
    """Start Telegram bot."""
    redis_db = Redis(
            host=env_settings.redis_host,
            port=env_settings.redis_port,
            password=env_settings.redis_password
        )

    bot_token = env_settings.tg_bot_token
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data[BOT_DATA_REDIS_DB] = redis_db

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handle_start)],

        states={
            BotState.MENU: [
                MessageHandler(
                    Filters.regex(NEW_QUESTION_TEXT),
                    handle_new_question_request,
                    pass_user_data=True
                )
            ],

            BotState.QUESTION: [
                MessageHandler(
                    Filters.regex(GIVE_UP_TEXT),
                    handle_give_up_request,
                    pass_user_data=True
                ),
                MessageHandler(
                    Filters.text & ~Filters.command,
                    handle_solution_attempt,
                    pass_user_data=True
                )
            ],
        },

        fallbacks=[ConversationHandler.END]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
