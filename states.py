from aiogram.dispatcher.filters.state import StatesGroup, State


class SocialNetwork(StatesGroup):
    STATE1 = State()  # vk
    STATE2 = State()  # inst
    STATE3 = State()  # admin
    STATE4 = State()  # setting hashtag for vk
    STATE5 = State()  # setting hashtag for instagram
