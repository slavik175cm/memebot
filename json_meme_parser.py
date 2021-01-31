# from urllib.request import urlopen
# from bs4 import BeautifulSoup
#
# html = open("htmldata.txt", "r")
# bsObj = BeautifulSoup(html)
# print(bsObj)
# # print(json.)

from vk_messages import MessagesAPI
import json
import requests

LOGIN = '+375447576345'
PASSWORD = 'slavvaa2014'
chat_id = 2000000000 + 84

login, password = LOGIN, PASSWORD
messages = MessagesAPI(login=login, password=password,
                                two_factor=False, cookies_save_path='sessions/')

kol = 0
batch_count = 0
while True:
    history = messages.method('messages.getHistory', user_id=chat_id, count=200, offset=batch_count * 200)
    # print(history)
    jsonHistory = json.loads(json.dumps(history))
    if len(jsonHistory['items']) == 0:
        break
    for i in range(len(jsonHistory['items'])):
        for j in range(len(jsonHistory['items'][i]['attachments'])):
            # print(jsonHistory['items'][i]['attachments'][j]['type'])
            if jsonHistory['items'][i]['attachments'][j]['type'] == 'photo':
                last = len(jsonHistory['items'][i]['attachments'][j]['photo']['sizes'])
                url = jsonHistory['items'][i]['attachments'][j]['photo']['sizes'][last - 1]['url'];
                # print(jsonHistory['items'][i]['attachments'][j]['photo']['sizes'][last - 1]['url'])

                response = requests.get(url)
                file = open("memes_from_c84\\" + str(kol) + ".png", "wb")
                kol += 1
                file.write(response.content)
                file.close()
    batch_count += 1

