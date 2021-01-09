"""Common functions to work with questions."""
import json
import random

from env_settings import env_settings


CHEAT_PHRASE = 'cheat'


def get_random_question() -> str:
    """Extract a random question from question data file."""
    with open(env_settings.questions_file) as questions_file:
        questions = json.load(questions_file)
        return random.choice(list(questions.keys()))


def get_answer(question) -> str:
    """Get answer for a question from question data file."""
    with open(env_settings.questions_file) as questions_file:
        questions = json.load(questions_file)
        return questions[question]


def is_correct_answer(user_answer: str, true_answer: str, cheating=False) -> bool:
    """
    Clean the answer from the question data file and compare with the given one.
    If cheating set to True, CHEAT_PHRASE considered as a correct answer.
    """
    if cheating and user_answer == CHEAT_PHRASE:
        return True

    exact_answer = true_answer
    if '(' in true_answer:
        exact_answer = true_answer.split('(')[0]
    if '.' in true_answer:
        exact_answer = true_answer.split('.')[0]
    exact_answer = exact_answer.rstrip()
    return user_answer == exact_answer
