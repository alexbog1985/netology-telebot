import random

from db import add_user, get_all_users
from settings import TG_TOKEN

from telebot import types, TeleBot, custom_filters
from telebot.storage import StateMemoryStorage
from telebot.handler_backends import State, StatesGroup


print('Start telegram bot...')

state_storage = StateMemoryStorage()
token_bot = TG_TOKEN
bot = TeleBot(token_bot, state_storage=state_storage)

userStep = {}
buttons = []


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово 🔙'
    NEXT = 'Дальше ⏭'


class MyStates(StatesGroup):
    target_word = State()
    translate_word = State()
    another_words = State()


def get_user_step(uid):
    # if uid in userStep:
    #     return userStep[uid]
    # else:
    #     known_users.append(uid)
    #     userStep[uid] = 0
    #     print("New user detected, who hasn't used \"/start\" yet")
    #     return 0


@bot.message_handler(commands=['cards', 'start'])
def start_bot(message):
    known_users = get_all_users()
    cid = message.chat.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    username = message.from_user.username
    print('Начинает сессию: ', f_name)

    if cid not in known_users:
        add_user(cid, f_name, l_name, username, user_step=0)
        bot.send_message(cid, "Hello, stranger, let study English...")

    markup = types.ReplyKeyboardMarkup(row_width=2)
    target_word = 'Peace'
    translate = 'Мир'
    target_word_btn = types.KeyboardButton(target_word)

    buttons = [target_word_btn]
    others = ['Green', 'White', 'Hello', 'Car']
    other_words_btns = [types.KeyboardButton(word) for word in others]
    buttons.extend(other_words_btns)
    random.shuffle(buttons)
    # next_btn = types.KeyboardButton(Command.NEXT)
    # add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    # delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    # buttons.extend([next_btn, add_word_btn, delete_word_btn])
    markup.add(*buttons)

    greeting = f"Выбери перевод слова:\n🇷🇺 {translate}"
    bot.send_message(message.chat.id, greeting, reply_markup=markup)

    # bot.set_state(message.from_user.id, MyStates.target_word, message.chat.id)
    # with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
    #     data['target_word'] = target_word
    #     data['translate_word'] = translate
    #     data['other_words'] = others


@bot.message_handler(func=lambda message: message.text == Command.NEXT)
def next_cards(message):
    create_cards(message)


@bot.message_handler(func=lambda message: message.text == Command.DELETE_WORD)
def delete_word(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data['target_word'])


@bot.message_handler(func=lambda message: message.text == Command.ADD_WORD)
def add_word(message):
    cid = message.chat.id
    userStep[cid] = 1


@bot.message_handler(func=lambda message: get_user_step(message.chat.id) == 1)
def save_new_word(message):
    pass


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        print(data)
        target_word = data['target_word']
    markup.add(*buttons)
    bot.send_message(message.chat.id, target_word, reply_markup=markup)


bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.infinity_polling(skip_pending=True)
