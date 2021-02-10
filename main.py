# -*- coding: utf-8 -*-
import telebot
import requests
import text_recognition as tr
import database_provider as db
import difflib
import os

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
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = os.path.join('.', 'photos', message.photo[-1].file_id + '.jpg')
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
        lst.append((get_text_coeff(key_words[i], text), paths[i]))
    lst.sort(reverse=True)
    print(lst)
    response = []
    for i in range(len(lst)):
        if lst[i][0] < 100 or len(response) == 3:
            break
        response.append(lst[i][1])

    return response


def get_text_coeff(text1, text2):
    words1 = text1.split(' ')
    words2 = text2.split(' ')
    response = 0
    for i in range(len(words2)):
        for j in range(len(words1)):
            aa = get_words_coeff(words1[j], words2[i])
            if not aa == 0:
                print(words2[i])
                print(words1[j])
                print(aa)
            response += aa
            # response += get_words_coeff(text1[j], text2[i])
    # print(words1)
    # print(words2)
    # print(response)
    return response


def get_words_coeff(word1, word2):
    if word1 == word2:
        return 1000

    for i in range(1, len(word2) // 2):
        if word2[i:] in word1 or word2[:-i] in word1:
            return 100

    return 0
bot.polling()

