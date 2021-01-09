Simple bot that plays quiz game with you.

## Set up:
Set environment variables:
* TELEGRAM_BOT_TOKEN - Telegram bot token. Can be obtained from [Bot Father](https://telegram.me/BotFather).
* VK_BOT_TOKEN - Vkontakte.ru bot token. Generated at the VK group administration panel.* GOOGLE_APPLICATION_CREDENTIALS - Path to a [GOOGLE_APPLICATION_CREDENTIALS file](https://cloud.google.com/docs/authentication/getting-started).
* REDIS_HOST - Redis DB hostname.
* REDIS_PORT - Redis DB port.
* REDIS_PASSWORD - Redis DB password.
* QUESTIONS_FILE - Path to a file where questions for the bot are stored (as a JSON)

## Usage:
* Run Telegram bot.
    > python run.py telegram_bot
* Run VK bot.
    > python run.py vk_bot

## Demo
 * Telegram version of a bot lives here - @ae_dvmn_support_bot
 * VK version - https://vk.com/club201440450