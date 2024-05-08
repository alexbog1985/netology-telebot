import telebot
import random
from telebot import types, custom_filters
from telebot.handler_backends import StatesGroup, State

from db import get_user, add_user, get_random_eng_word, get_user_words, delete_user_word, get_all_words, add_user_word, \
    add_new_word

from translate_api import translate


TG_TOKEN = "<KEY>" # Your token

bot = telebot.TeleBot(TG_TOKEN, state_storage=telebot.storage.StateMemoryStorage())  # создание бота


class Command:
    ADD_WORD = 'Добавить слово ➕'
    DELETE_WORD = 'Удалить слово 🔙'
    NEXT = 'Дальше ⏭'
    LEARN = 'Ну что, начнём ⬇️'


class MyStates(StatesGroup):
    rus_word = State()
    target_eng_word = State()
    other_eng_words = State()
    delete_word = State()
    add_word = State()


user_step = {}


@bot.message_handler(commands=['cards', 'start'])
def start(message):

    cid = message.chat.id
    f_name = message.from_user.first_name
    l_name = message.from_user.last_name
    user_id = message.from_user.id
    username = message.from_user.username

    if get_user(cid) is None:
        add_user(cid, user_id, f_name, l_name, username, step=0)
        bot.send_message(cid, f'Привет, {f_name} {l_name}! Я помогу тебе выучить английский язык.')

    markup = types.ReplyKeyboardMarkup(row_width=2)

    go_btn = types.KeyboardButton(Command.LEARN)
    markup.add(go_btn)
    bot.send_message(cid, 'Поехали?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == Command.LEARN, content_types=['text'])
def learn(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)

    words = get_user_words(message.from_user.id)
    if words:
        rus_word = words['rus_word']  # Русское слово
        target_eng_word = words['eng_word']  # Правильное английское слово
        target_eng_word_button = types.KeyboardButton(target_eng_word)  # создание кнопки
        other_eng_words = []  # другие, неправильные английские слова
        while len(other_eng_words) < 3:
            random_eng_word = get_random_eng_word()
            if random_eng_word not in other_eng_words and random_eng_word != target_eng_word:
                other_eng_words.append(random_eng_word)

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
    else:
        bot.send_message(message.chat.id, 'У вас нет слов для изучения. '
                                          'Добавьте новое слово. '
                                          'Введите слово на русском языке.')
        bot.register_next_step_handler(message, add_word)


@bot.message_handler(state=MyStates.delete_word, content_types=['text'])
def delete_word(message):

    bot.set_state(message.from_user.id, MyStates.delete_word, message.chat.id)
    markup = types.ReplyKeyboardMarkup(row_width=2)
    yes_btn = types.KeyboardButton('Да')
    no_btn = types.KeyboardButton('Нет')
    markup.add(yes_btn, no_btn)

    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        eng_word = data['target_eng_word']
        rus_word = data['rus_word']
    bot.send_message(message.chat.id, f'Вы точно хотите удалить "{rus_word}"?:', reply_markup=markup)
    if message.text == 'Да':
        bot.send_message(message.chat.id, f'Удалил слово "{rus_word}" перевод: "{eng_word}"')
        delete_user_word(message.from_user.id, eng_word)
        learn(message)
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Окей, не удалял.')
        learn(message)


@bot.message_handler(state=MyStates.add_word)
def add_word(message):
    cid = message.from_user.id
    dict_words = get_all_words()
    bot.set_state(message.from_user.id, MyStates.add_word, message.chat.id)
    if message.text.lower() in dict_words:
        add_user_word(cid, dict_words[message.text.lower()])
        learn(message)
    else:
        rus_word = message.text.lower()
        eng_word = translate(rus_word)
        add_new_word(rus_word, eng_word)
        add_user_word(cid, eng_word)
        learn(message)


@bot.message_handler(state=MyStates.rus_word, content_types=['text'])
def message_reply(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        target_eng_word = data['target_eng_word']
    if message.text == target_eng_word:
        bot.send_message(message.chat.id, f'Правильно!')
        learn(message)
    elif message.text == Command.NEXT:
        learn(message)
    elif message.text == Command.ADD_WORD:
        bot.send_message(message.chat.id, 'Введите слово для добавления:')
        bot.register_next_step_handler(message, add_word)
    elif message.text == Command.DELETE_WORD:
        delete_word(message)
    else:
        bot.send_message(message.chat.id, 'Ошибка! Попробуйте еще раз.')


@bot.message_handler(state=None)
def none_state(message):
    start(message)


bot.add_custom_filter(custom_filters.StateFilter(bot))

if __name__ == '__main__':
    print('Bot started')
    bot.polling(none_stop=True)

