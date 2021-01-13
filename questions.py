"""Common functions to work with questions."""
import pathlib
import json
import random
import logging
from typing import Tuple


CHEAT_PHRASE = 'cheat'
PARSE_QUESTIONS_FILE_TIMEOUT = 5


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()


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


def _parse_block(block: str) -> Tuple[str, str]:
    """Extract question and answer from a text block."""
    question_start = block.find('\n', block.find('Вопрос')) + 1
    question_end = block.find('\n\n', question_start)
    question = block[question_start:question_end]
    question = " ".join(question.split())

    answer_start = block.find('\n', block.find('Ответ')) + 1
    end_symbols_positions = [position for position in (
        block.find('.', answer_start),
        block.find('(', answer_start),
        block.find('\n', answer_start)
    ) if position != -1]  # position is -1 if the symbol is not in the block.
    answer_end = min(end_symbols_positions) if end_symbols_positions else -1
    answer = block[answer_start:answer_end].strip()

    return question, answer


def parse_questions(raw_data_folder: str, parsed_questions_file: str) -> None:
    """Parse raw questions data and write parsed data to a file."""
    raw_data_folder_content = pathlib.Path(raw_data_folder).glob('**/*')
    question_files_list = [item for item in raw_data_folder_content if item.is_file()]

    questions = dict()

    for questions_file_name in question_files_list:
        with open(questions_file_name, 'r', encoding='KOI8-R') as questions_file:
            questions_file_blocks = questions_file.read().split('\n\n\n')
            for block in questions_file_blocks:
                if 'Вопрос' in block and 'Ответ' in block:
                    question, answer = _parse_block(block)

                questions[question] = answer
            logger.info(f'File {questions_file_name} parsed')

    with open(parsed_questions_file, 'w') as output_file:
        output_file.write(json.dumps(questions, ensure_ascii=False, indent=2))
