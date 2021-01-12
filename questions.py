"""Common functions to work with questions."""
import json
import random


CHEAT_PHRASE = 'cheat'


class QuizDB:
    """Class to work with questions JSON file."""
    def __init__(self, questions_file):
        with open(questions_file) as questions:
            self._questions = json.load(questions)

    def get_random_question(self) -> str:
        """Extract a random question from question data file."""
        return random.choice(list(self._questions.keys()))

    def get_answer(self, question) -> str:
        """Get answer for a question from question data file."""
        return self._questions[question]


def is_correct_answer(user_answer: str, true_answer: str, cheating=False) -> bool:
    """
    Compare user's answer and a true answer.
    If cheating set to True, CHEAT_PHRASE considered as a correct answer.
    """
    if cheating and user_answer == CHEAT_PHRASE:
        return True

    return user_answer.lower() == true_answer.lower()
