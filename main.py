from datetime import datetime, timezone
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from emojis import encode
from requests import get
import json
import requests
import aiogram
from states import SocialNetwork
from config import TOKEN, access_token
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from instagram.searchPostsInst import searchPosts
from instagram.getLikersInst import getLikers
from getHeaders import gettingHeaders
from vk.getLikersVKfinal import tryGettingPage, getPostsToLike, translateToID
from config import hashtagInst, hashtagVk


bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

greetings = encode(
    'Привет! :muscle: Я помогаю получать взаимные лайки на посты, для того чтобы получить заветный хэштэг, который можно указать в посте и все остальные смогут его пролайкать, нужно будет лайкнуть другие участвующие в задании посты. Если готовы, то начнем: нажмите кнопку /получить_тэг')
s = requests.Session()

addChannelButton0 = "/получить_тэг"
addChannelButton1 = "/vk"
addChannelButton2 = "/inst"
addChannelButton3 = "/return"

button0 = KeyboardButton(addChannelButton0)
button1 = KeyboardButton(addChannelButton1)
button2 = KeyboardButton(addChannelButton2)
button3 = KeyboardButton(addChannelButton3)
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
return_only = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
network_choice = ReplyKeyboardMarkup(
    resize_keyboard=True, one_time_keyboard=True)
greet_kb.add(button0)
network_choice.add(button1)
network_choice.add(button2)
network_choice.add(button3)
return_only.add(button3)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(greetings, reply_markup=greet_kb)


@dp.message_handler(state='*', commands=['return'])
async def process_setstate_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await state.reset_state()
    await message.reply(greetings, reply_markup=greet_kb)


@dp.message_handler(commands=['получить_тэг'])
async def process_start_command(message: types.Message):
    await message.reply("нажмите кнопку vk или inst, где нужны лайки", reply_markup=network_choice)


@dp.message_handler(commands=['vk'])
async def process_start_command(message: types.Message):
    await SocialNetwork.STATE1.set()
    await bot.send_message(message.from_user.id, "напишите id или короткое имя аккаунта vk, с которого будете лайкать посты участников\nПример: myshortname")

# for Vk.com ###


@dp.message_handler(state=SocialNetwork.STATE1)
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
# обработка случая с числовым id
    if message.text.isdigit():
        await bot.send_message(message.from_user.id, 'подожди чуть-чуть, пока я проверю этот аккаунт')
        userObj = tryGettingPage(message.text, access_token)
        if len(userObj['response']) == 0:
            await bot.send_message(message.from_user.id, encode("пришлите, пожалуйста, ваш действующий id :no_mouth:\nмне нужны только его цифры, либо ваше короткое имя без @"))
        elif userObj['response'][0]['first_name'] == 'DELETED':
            await bot.send_message(message.from_user.id, encode("пришлите, пожалуйста, ваш действующий id :no_mouth:\nмне нужны только его цифры, либо ваше короткое имя без @"))
        else:
            arrayOfPosts = getPostsToLike(int(message.text))
            if len(arrayOfPosts) == 0:
                await bot.send_message(message.from_user.id, encode(f"все пролайкано! :white_check_mark:\nдержи тэг: #{hashtagVk}\nрекомендую добавить и другие тэги(#лайки #новое #взаимно #абсолютно #классный),чтобы нечестные пользователи не получали лайки ничего не лайкнув:innocent:"))
                await state.reset_state()
            else:
                await bot.send_message(message.from_user.id, f"пролайкай следующие посты и я дам тэг, с которым ты получишь лайки!")
                a = ""
                for element in arrayOfPosts:
                    a += f"{element}\n"
                await bot.send_message(message.from_user.id, a, disable_web_page_preview=True)
                await state.reset_state()
    else:
        await bot.send_message(message.from_user.id, 'подожди чуть-чуть, пока я проверю этот аккаунт')
# обработка случая с коротким именем пользователя
        id = translateToID(message.text, access_token)
        if id == None:
            await bot.send_message(message.from_user.id, encode("пришлите, пожалуйста, ваш действующий id :no_mouth:\nмне нужны только его цифры, либо ваше короткое имя без @"))
        else:
            arrayOfPosts = getPostsToLike(int(id))
            if len(arrayOfPosts) == 0:
                await bot.send_message(message.from_user.id, encode(f"все пролайкано! :white_check_mark:\nдержи тэг: #{hashtagVk}\nрекомендую добавить и другие тэги(#лайки #новое #взаимно #абсолютно #классный),чтобы нечестные пользователи не получали лайки ничего не лайкнув:innocent:"))
            else:
                await bot.send_message(message.from_user.id, encode(f"пролайкай следующие посты и я дам тэг :trophy:, с которым ты получишь лайки!"))
                a = ""
                for element in arrayOfPosts:
                    a += f"{element}\n"
                await bot.send_message(message.from_user.id, a, disable_web_page_preview=True)
            await state.reset_state()
#


@dp.message_handler(commands=['inst'])
async def process_start_command(message: types.Message):
    await SocialNetwork.STATE2.set()
    await bot.send_message(message.from_user.id, "напишите свой ник instagram аккаунта, с которого будете лайкать посты участников\nПример: myshortname")

# for instagram ###


@dp.message_handler(state=SocialNetwork.STATE2)
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    await bot.send_message(message.from_user.id, 'подожди чуть-чуть, пока я проверю этот аккаунт')
    username = message.text
    postsToLike = []
    arrayOfPosts = searchPosts(hashtag=hashtagInst)
    for element in arrayOfPosts:
        arrayOfLikers = getLikers(element[0])
        if username in arrayOfLikers:
            continue
        else:
            postsToLike.append(element[1])
    if len(postsToLike):
        await bot.send_message(message.from_user.id, encode(f"пролайкай следующие посты и я дам хэштэг :trophy:, с которым ты получишь лайки!"))
        answerString = ''
        for el in postsToLike:
            answerString += el + '\n'
        await bot.send_message(message.from_user.id, answerString, disable_web_page_preview=True)
    else:
        await bot.send_message(message.from_user.id, encode(f"все пролайкано! :white_check_mark:\nдержи тэг: #{hashtagInst}\nрекомендую добавить и другие тэги(#лайки #новое #взаимно #абсолютно #классный),чтобы нечестные пользователи не получали лайки ничего не лайкнув:innocent:"))
    await state.reset_state()
#


@dp.message_handler(commands=['admin101'])
async def process_start_command(message: types.Message):
    await SocialNetwork.STATE3.set()
    await message.reply("вы в режиме админа, выберите соцсеть для которой будете устанавливать хэштэг", reply_markup=network_choice)

# for admin ###


@dp.message_handler(state=SocialNetwork.STATE3)
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    if message.text == '/vk':
        await SocialNetwork.STATE4.set()
        await message.reply("напишите новый хэштэг для вк", reply_markup=return_only)
    elif message.text == '/inst':
        await SocialNetwork.STATE5.set()
        await message.reply("напишите новый хэштэг для вк", reply_markup=return_only)
    elif message.text == '/return':
        await state.reset_state()
        await message.reply(greetings, reply_markup=greet_kb)
    else:
        await state.reset_state()
        await message.reply("попробуйте снова", reply_markup=greet_kb)

#
# change hashtag vk


@dp.message_handler(state=SocialNetwork.STATE4)
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    global hashtagVk
    hashtagVk = message.text
    await message.reply(f"вы успешно сменили хэштэг на {message.text} для вк", reply_markup=greet_kb)
    await state.reset_state()
#
# changing hashtag inst


@dp.message_handler(state=SocialNetwork.STATE5)
async def process_start_command(message: types.Message):
    state = dp.current_state(user=message.from_user.id)
    global hashtagInst
    hashtagInst = message.text
    await message.reply(f"вы успешно сменили хэштэг на {message.text} для instagram", reply_markup=greet_kb)
    await state.reset_state()
#
# handler for all else


@dp.message_handler()
async def process_start_command(message: types.Message):
    await message.reply("постарайтесь следовать инструкциям в сообщениях", reply_markup=greet_kb)
#


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == "__main__":

    executor.start_polling(dp, on_shutdown=shutdown)
