"""VK version of Quiz Bot."""
from redis import Redis
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.vk_api import VkApiMethod
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

from env_settings import env_settings
from questions import (get_random_question, get_answer, is_correct_answer,
                       NEW_QUESTION_TEXT, GIVE_UP_TEXT, SCORE_TEXT)


def handle_new_player(event: Event, vk_api: VkApiMethod):
    keyboard = VkKeyboard()
    keyboard.add_button(NEW_QUESTION_TEXT, color=VkKeyboardColor.PRIMARY)
    keyboard.add_button(GIVE_UP_TEXT, color=VkKeyboardColor.NEGATIVE)
    keyboard.add_line()
    keyboard.add_button(SCORE_TEXT)

    vk_api.messages.send(
        user_id=event.user_id,
        message=f'Добрый день! Нажмите "{NEW_QUESTION_TEXT}" для начала игры.',
        random_id=get_random_id(),
        keyboard=keyboard.get_keyboard(),
    )


def handle_new_question_request(event, vk_api, redis_db):
    question = get_random_question()
    redis_db.set(event.user_id, question)
    vk_api.messages.send(
        user_id=event.user_id,
        message=question,
        random_id=get_random_id()
    )


def handle_give_up_request(event, vk_api, redis_db):
    question = redis_db.get(event.user_id).decode('utf-8')
    answer = get_answer(question)
    vk_api.messages.send(
        user_id=event.user_id,
        message=f'Правильный ответ: "{answer}"',
        random_id=get_random_id()
    )

    new_question = get_random_question()
    redis_db.set(event.user_id, new_question)
    vk_api.messages.send(
        user_id=event.user_id,
        message=new_question,
        random_id=get_random_id()
    )


def handle_solution_attempt(event, vk_api, redis_db):
    question = redis_db.get(event.user_id).decode('utf-8')
    answer = get_answer(question)
    if is_correct_answer(event.message, answer, cheating=True):
        reply_text = 'Поздравляем! Ответ верен. Ещё разок?'
    else:
        reply_text = f'Неправильно :( Правильный ответ - "{answer}". Хотите попробовать ещё раз?'
    vk_api.messages.send(
        user_id=event.user_id,
        message=reply_text,
        random_id=get_random_id()
    )


def handle_score_request(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message='Десять Вассерманов из десяти. Вы великолепны!',
        random_id=get_random_id()
    )


def handle_event(event, vk_api, redis_db):
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.text == NEW_QUESTION_TEXT:
            handle_new_question_request(event, vk_api, redis_db)
        elif event.text == GIVE_UP_TEXT:
            handle_give_up_request(event, vk_api, redis_db)
        elif event.text == SCORE_TEXT:
            handle_score_request(event, vk_api)
        elif redis_db.get(event.user_id) is None:
            handle_new_player(event, vk_api)
        else:
            handle_solution_attempt(event, vk_api, redis_db)


def start_bot() -> None:
    """Start VK bot."""
    session = VkApi(token=env_settings.vk_bot_token)
    vk_api = session.get_api()
    longpoll = VkLongPoll(session)

    redis_db = Redis(
            host=env_settings.redis_host,
            port=env_settings.redis_port,
            password=env_settings.redis_password
        )

    for event in longpoll.listen():
        handle_event(event, vk_api, redis_db)
