"""Module to work with environment variables."""
from dataclasses import dataclass

from environs import Env


@dataclass
class EnvSettings:
    """Environment settings for Quiz Bot."""
    tg_bot_token: str
    vk_bot_token: str
    vk_language_code: str
    redis_host: str
    redis_port: int
    redis_password: str
    questions_file: str


def get_env_settings() -> EnvSettings:
    """Read environment settings."""
    env = Env()
    env.read_env()
    return EnvSettings(
        tg_bot_token=env('TELEGRAM_BOT_TOKEN', None),
        vk_bot_token=env('VK_BOT_TOKEN', None),
        vk_language_code=env('VK_LANGUAGE_CODE', None),
        redis_host=env('REDIS_HOST', None),
        redis_port=env.int('REDIS_PORT', None),
        redis_password=env('REDIS_PASSWORD', None),
        questions_file=env('QUESTIONS_FILE', None)
    )


env_settings = get_env_settings()
