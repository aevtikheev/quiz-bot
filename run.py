"""Entry point to operate with Quiz Bot."""
import argparse
import logging
import sys

import telegram_bot
import vk_bot
from questions import parse_questions

CMD_TELEGRAM_BOT = 'telegram_bot'
CMD_VK_BOT = 'vk_bot'
CMD_PARSE_QUESTIONS = 'parse_questions'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(CMD_TELEGRAM_BOT, help='Run telegram bot')
    subparsers.add_parser(CMD_VK_BOT, help='Run VK bot')

    questions_parser = subparsers.add_parser(CMD_PARSE_QUESTIONS, help='Parse raw questions data')
    questions_parser.add_argument(
        '-q', '--questions_folder', type=str,
        help='Folder with question\'s raw data',
        required=True
    )
    questions_parser.add_argument(
        '-f', '--output_file', type=str,
        help='File where parsed questions will be stored',
        required=True
    )

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    return parser.parse_args()


def main() -> None:
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    args = parse_args()
    if args.command == CMD_TELEGRAM_BOT:
        telegram_bot.start_bot()
    elif args.command == CMD_VK_BOT:
        vk_bot.start_bot()
    elif args.command == CMD_PARSE_QUESTIONS:
        parse_questions(args.questions_folder, args.output_file)


if __name__ == '__main__':
    main()
