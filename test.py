#
# import vk_api
# import requests
# vk_chat_const = 2000000000
# api = 'https://api.vk.com/method/'
#
# LOGIN = '+375447576345'
# PASSWORD = 'slavvaa2014'
# chat_id = 2000000000 + 84
# vk_session = vk_api.VkApi(LOGIN, PASSWORD)
#
#
# try:
#     vk_session.auth()
#     print("success")
# except vk_api.AuthError as error_msg:
#     print(error_msg)
#     print("damn")
#
# print(vk_session.token)
# access_token = vk_session.token.__getitem__('access_token')
# start_from = 0
#
# attachments = requests.get(api + 'messages.getHistoryAttachments', params = {'access_token':access_token,
#                                                                             'peer_id':chat_id,
#                                                                             'media_type':'photo',
#                                                                             'start_from':start_from,
#                                                                             'count':200,
#                                                                             'v':5.126,
#                                                                             'photo_sizes':0})
# print(attachments.text)

import difflib
print(difflib.SequenceMatcher("lama", "lama").ratio())