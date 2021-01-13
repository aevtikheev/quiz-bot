"""Telegram version of Quiz Bot."""
from enum import Enum

from redis import Redis
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext, ConversationHandler)

from env_settings import env_settings
from questions import QuizDB, is_correct_answer
from bot_text import NEW_QUESTION_TEXT, GIVE_UP_TEXT, SCORE_TEXT


BOT_DATA_USERS_DB_KEY = 'redis_db'
BOT_DATA_QUIZ_DB_KEY = 'quiz_db'


class BotState(Enum):
    MENU = 1
    QUESTION = 2


def handle_start(update: Update, context: CallbackContext) -> BotState:
    """Handle /start command, Show menu buttons and greeting."""
    menu_buttons = [[NEW_QUESTION_TEXT, GIVE_UP_TEXT], [SCORE_TEXT]]
    reply_markup = ReplyKeyboardMarkup(menu_buttons)
    update.message.reply_text(
        f'Добрый день! Нажмите "{NEW_QUESTION_TEXT}" для начала игры.',
        reply_markup=reply_markup
    )

    return BotState.MENU


def handle_new_question_request(update: Update, context: CallbackContext) -> BotState:
    """Send new question to the player."""
    users_db = context.bot_data[BOT_DATA_USERS_DB_KEY]
    quiz_db = context.bot_data[BOT_DATA_QUIZ_DB_KEY]

    question = quiz_db.get_random_question()
    users_db.set(update.effective_user.id, question)
    update.message.reply_text(question)

    return BotState.QUESTION


def handle_solution_attempt(update: Update, context: CallbackContext) -> BotState:
    """Check the answer. If it's correct, send congrats, else show the right answer."""
    users_db = context.bot_data[BOT_DATA_USERS_DB_KEY]
    quiz_db = context.bot_data[BOT_DATA_QUIZ_DB_KEY]

    question = users_db.get(update.effective_user.id).decode('utf-8')
    answer = quiz_db.get_answer(question)
    if is_correct_answer(update.message.text, answer):
        reply_text = 'Поздравляем! Ответ верен. Ещё разок?'
    else:
        reply_text = f'Неправильно :( Правильный ответ - "{answer}". Хотите попробовать ещё раз?'
    update.message.reply_text(reply_text)

    return BotState.MENU


def handle_give_up_request(update: Update, context: CallbackContext) -> BotState:
    """Show the correct answer and ask a new one."""
    users_db = context.bot_data[BOT_DATA_USERS_DB_KEY]
    quiz_db = context.bot_data[BOT_DATA_QUIZ_DB_KEY]

    question = users_db.get(update.effective_user.id).decode('utf-8')
    answer = quiz_db.get_answer(question)
    update.message.reply_text(f'Правильный ответ: "{answer}"')

    new_question = quiz_db.get_random_question()
    users_db.set(update.effective_user.id, new_question)
    update.message.reply_text(new_question)

    return BotState.QUESTION


def handle_score_request(update: Update, context: CallbackContext) -> int:
    """Show the overall score for the player."""
    update.message.reply_text('Десять Вассерманов из десяти. Вы великолепны!')

    return ConversationHandler.END


def start_bot() -> None:
    """Start Telegram bot."""
    users_db = Redis(
            host=env_settings.redis_host,
            port=env_settings.redis_port,
            password=env_settings.redis_password
        )
    quiz_db = QuizDB(env_settings.questions_file)

    bot_token = env_settings.tg_bot_token
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data[BOT_DATA_USERS_DB_KEY] = users_db
    dispatcher.bot_data[BOT_DATA_QUIZ_DB_KEY] = quiz_db

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', handle_start)],

        states={
            BotState.MENU: [
                MessageHandler(
                    Filters.regex(NEW_QUESTION_TEXT),
                    handle_new_question_request,
                    pass_user_data=True
                ),
                MessageHandler(
                    Filters.regex(SCORE_TEXT),
                    handle_score_request,
                    pass_user_data=True
                ),
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
                ),
            ],
        },

        fallbacks=[ConversationHandler.END]
    )
    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
