"""TODO"""
import json
import random

from env_settings import env_settings


def get_random_question():
    """TODO"""
    with open(env_settings.questions_file) as questions_file:
        questions = json.load(questions_file)
        return random.choice(list(questions.items()))
