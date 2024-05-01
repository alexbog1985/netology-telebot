import telebot
import random
from telebot import types
from telebot.handler_backends import StatesGroup, State

from db import get_all_users, add_user

from settings import TG_TOKEN  # токен бота

bot = telebot.TeleBot(TG_TOKEN)  # создание бота

known_users = get_all_users()  # получение всех пользователей


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово 🔙'
    NEXT = 'Дальше ⏭'


class MyStates(StatesGroup):
    rus_word = State()
    target_eng_word = State()
    other_eng_words = State()


@bot.message_handler(commands=['cards', 'start'])
def start(message):
    cid = message.chat.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    user_id = message.from_user.id
    username = message.from_user.username
    print(known_users)

    if cid not in known_users:
        add_user(cid, user_id, f_name, l_name, username, step=0)
        bot.send_message(cid, f'Привет, {f_name} {l_name}! Я помогу тебе выучить английский язык.')

    markup = types.ReplyKeyboardMarkup(row_width=2)

    rus_word = 'Мир'  # Русское слово
    target_eng_word = 'Peace'  # Правильное английское слово
    target_eng_word_button = types.KeyboardButton(target_eng_word)  # создание кнопки
    other_eng_words = ['Green', 'Car', 'Hello']  # другие, неправильные английские слова
    other_eng_word_buttons = [types.KeyboardButton(word) for word in other_eng_words]  # создание кнопок

    buttons = [target_eng_word_button] + other_eng_word_buttons  # список кнопок с ответами
    random.shuffle(buttons)  # перемешивание кнопок

    next_btn = types.KeyboardButton(Command.NEXT)
    add_word_btn = types.KeyboardButton(Command.ADD_WORD)
    delete_word_btn = types.KeyboardButton(Command.DELETE_WORD)
    buttons.extend([next_btn, add_word_btn, delete_word_btn])

    markup.add(*buttons)

    bot.send_message(message.chat.id, f'Выберите перевод слова "{rus_word}":', reply_markup=markup)

    bot.set_state(message.from_user.id, MyStates.rus_word, message.chat.id)
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['rus_word'] = rus_word
        data['target_eng_word'] = target_eng_word
        data['other_eng_words'] = other_eng_words


@bot.message_handler(func=lambda message: True, content_types=['text'])
def message_reply(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_eng_word = data['target_eng_word']
    if message.text == target_eng_word:
        bot.send_message(message.chat.id, 'Правильно!')
    elif message.text == Command.NEXT:
        pass
    elif message.text == Command.ADD_WORD:
        pass
    elif message.text == Command.DELETE_WORD:
        pass
    else:
        bot.send_message(message.chat.id, 'Ошибка!')


if __name__ == '__main__':
    print('Bot started')
    bot.polling(none_stop=True)