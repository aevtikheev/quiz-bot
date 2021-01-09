"""TODO"""
import json
import random

from env_settings import env_settings


NEW_QUESTION_TEXT = 'Новый вопрос'
GIVE_UP_TEXT = 'Сдаться'
SCORE_TEXT = 'Мой счёт'

CHEAT_PHRASE = 'cheat'


def get_random_question():
    """TODO"""
    with open(env_settings.questions_file) as questions_file:
        questions = json.load(questions_file)
        return random.choice(list(questions.keys()))


def get_answer(question):
    """TODO"""
    with open(env_settings.questions_file) as questions_file:
        questions = json.load(questions_file)
        return questions[question]


def is_correct_answer(user_answer, true_answer, cheating=False):
    """TODO"""
    if cheating and user_answer == CHEAT_PHRASE:
        return True

    exact_answer = true_answer
    if '(' in true_answer:
        exact_answer = true_answer.split('(')[0]
    if '.' in true_answer:
        exact_answer = true_answer.split('.')[0]
    exact_answer = exact_answer.rstrip()
    return user_answer == exact_answer
