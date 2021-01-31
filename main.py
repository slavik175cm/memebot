# -*- coding: utf-8 -*-
import telebot
import text_recognition as tr
import database_provider as db
import difflib

TOKEN = '1591401263:AAECT7GwBHbB8nrB9Ds7Q49J8LwUxbYvR68'
bot = telebot.TeleBot(TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Добавить мем', 'Найти мем(ы)', 'Настройки')


@bot.message_handler(commands=['start'])
def start_message(message):
    db.add_new_user(message.chat.id)
    bot.send_message(message.chat.id, 'Привет, ты написал мнее /start')


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'Привет':
        bot.send_message(message.chat.id, 'Привет, мой создатель', reply_markup=keyboard1)
    elif message.text == 'Пока':
        bot.send_message(message.chat.id, 'Прощай, создатель')
    elif message.text == 'Добавить мем':
        bot.send_message(message.chat.id, 'Загрузите картинку или файл')
    else:
        memes_paths = get_n_closest(message.chat.id, message.text)
        for meme_path in memes_paths:
            bot.send_photo(message.chat.id, open(meme_path, 'rb'))
        # bot.send_message(message.chat.id, get_n_closest(message.chat.id, message.text))


@bot.message_handler(content_types=['photo'])
def send_meme(message):
    import requests
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'D:\\PycharmProjects\\MemeBot\\photos\\' + message.photo[-1].file_id + '.jpg'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    tr.change_lang(tr.Lang.ENG)
    reply = list_to_string(tr.get_text_from_meme(src))
    tr.change_lang(tr.Lang.RUS)
    reply += '\n' + list_to_string(tr.get_text_from_meme(src))

    bot.reply_to(message, "Фото добавлено\n" + reply)
    db.add_new_meme(message.chat.id, src, reply)


def list_to_string(s):
    str1 = " "
    return str1.join(s)


def get_n_closest(user_id, text):
    paths, key_words = db.get_user_memes(user_id)
    lst = []
    for i in range(len(paths)):
        lst.append((difflib.SequenceMatcher(None, key_words[i], text).ratio() * (len(key_words[i]) + len(text)), paths[i]))
    lst.sort(reverse=True)
    print(lst)
    response = []
    for i in range(len(lst)):
        if lst[i][0] < 6.0 or len(response) == 3:
            break
        response.append(lst[i][1])

    return response


bot.polling()

