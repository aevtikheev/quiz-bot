"""VK version of Quiz Bot."""
import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, Event
from vk_api.vk_api import VkApiMethod

from env_settings import env_settings


def start_bot() -> None:
    """Start VK bot."""
    session = vk_api.VkApi(token=env_settings.vk_bot_token)
    api = session.get_api()
    longpoll = VkLongPoll(session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            ...
