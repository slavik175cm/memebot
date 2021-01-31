# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# html = urlopen("https://vk.com/im?peers=435799447&sel=c84&w=historyc84_photo")
# bsObj = BeautifulSoup(html.read())
# print(bsObj.body)

import vk_api
import urllib
import requests
import json
import time
import sys
import os
import datetime
import urllib.request
vk_chat_const = 2000000000
api = 'https://api.vk.com/method/'

LOGIN = '+375447576345'
PASSWORD = 'slavvaa2014'
chat_id = 2000000000 + 84
vk_session = vk_api.VkApi(LOGIN, PASSWORD)


try:
    vk_session.auth()
    print("success")
except vk_api.AuthError as error_msg:
    print(error_msg)
    print("damn")

print(vk_session.token)
access_token = vk_session.token.__getitem__('access_token')
start_from = 0
#
#
# vk = vk_session.get_api()
#
#
#
attachments = requests.get(api + 'messages.getHistoryAttachments', params = {'access_token':access_token,
                                                                            'peer_id':chat_id,
                                                                            'media_type':'photo',
                                                                            'start_from':start_from,
                                                                            'count':200,
                                                                            'v':5.126,
                                                                            'photo_sizes':0})
print(attachments.text)
# access_key_url = 'https://oauth.vk.com/authorize'
# get_key = requests.get(access_key_url, params = {'client_id': 5804682,
#                                                 'redirect_uri':'https://oauth.vk.com/blank.html',
#                                                 'scope':'messages',
#                                                 'response_type':'token'})
# print(get_key.url)

# https://oauth.vk.com/authorize?client_id=165761314&redirect_uri=https://oauth.vk.com/blank.html&scope=photos&response_type=token
