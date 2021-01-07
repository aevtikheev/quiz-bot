"""Entry point to operate with a Quiz Bot."""
import argparse
import sys

import telegram_bot
import vk_bot


CMD_TELEGRAM_BOT = 'telegram_bot'
CMD_VK_BOT = 'vk_bot'


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    subparsers.add_parser(CMD_TELEGRAM_BOT, help='Run telegram bot')
    subparsers.add_parser(CMD_VK_BOT, help='Run VK bot')

    if len(sys.argv) <= 1:
        sys.argv.append('--help')

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == CMD_TELEGRAM_BOT:
        telegram_bot.start_bot()
    elif args.command == CMD_VK_BOT:
        vk_bot.start_bot()


if __name__ == '__main__':
    main()
