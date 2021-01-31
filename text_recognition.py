import numpy as np
import cv2
import pytesseract
from PIL import Image
import enchant
from enum import Enum

eng_enchant_checker = enchant.Dict("en_US")
rus_enchant_checker = enchant.Dict("ru_RU")

eng_whitelist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
rus_whitelist = "йцукеёнгшщзхъфывапролджэячсмитьбюЙЦУКЕЁНГШЩЗХЪФЫАПРОЛДЖЭЯЧСМИТЬБЮ1234567890"


class Lang(Enum):
    ENG = 1
    RUS = 2


def change_lang(new_lang):
    global enchant_checker
    global whitelist
    global lang

    if new_lang is Lang.ENG:
        enchant_checker = eng_enchant_checker
        whitelist = eng_whitelist
        lang = "eng"

    else:
        enchant_checker = rus_enchant_checker
        whitelist = rus_whitelist
        lang = "rus"


def process_clean_image(img):
    custom_config = r"--psm 11"
    text = pytesseract.image_to_data(img, lang=lang, config=custom_config, output_type='data.frame')
    # print(text)
    response = []
    j = 0
    for i in text["text"]:
        if text["conf"][j] == -1:
            j += 1
            continue
        word = get_clean_word(str(i))
        conf = text["conf"][j]
        if is_word_ok(word, conf):
            response.append(word)
        j += 1
    return response


def get_clean_word(word):
    clean_word = ''
    for char in word:
        if char in whitelist:
            clean_word += char
    return clean_word.lower()


def is_word_ok(word, conf):
    if len(word) > 2 and conf >= 90:
        return True

    if len(word) <= 2 or conf < 70:
        return False

    return enchant_checker.check(word)


def process_grey_image(im, thresvalue, type):
    _, im1 = cv2.threshold(im, thresvalue, 255, type)
    return process_clean_image(im1)


def get_text_from_meme(path_to_meme, step=23):
    im = np.array(Image.open(path_to_meme))
    im = cv2.bilateralFilter(im, 5, 55, 60)
    try:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    except:
        pass
    answer = []
    for i in range(5, 250, step):
        answer.extend(process_grey_image(im, i, cv2.THRESH_BINARY_INV))
    return list(set(answer))


# change_lang(Lang.ENG)
# print(get_text_from_meme(src_path + image_name))
# change_lang(Lang.RUS)
# print(get_text_from_meme(src_path + image_name))
# for i in range(3, 100, 5):
#     print("step " + str(i) + ":")
#     print(get_text_from_meme(src_path, image_name, i))



