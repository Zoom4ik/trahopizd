# -*- coding: utf8 -*-
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType
import vk_api.upload
from time import sleep
import random
from python3_anticaptcha import ImageToTextTask
from python3_anticaptcha import errors
import requests
import json
import traceback
from CONFIG import info

def captcha_handler(captcha):
    ''' Отлавливание каптчи
    :param captcha: Объект капчи
    :return: Новая_попытка_отправить_сообщение_с_введенной_капчей
    '''
    key = ImageToTextTask.ImageToTextTask(anticaptcha_key=info.captcha, save_format='const') \
            .captcha_handler(captcha_link=captcha.get_url())


    # Пробуем снова отправить запрос с капчей
    return captcha.try_again(key['solution']['text'])


vk_session = vk_api.VkApi(token=info.token, captcha_handler=captcha_handler)

vk = vk_session.get_api()

titlel = info.titlel

def send_message(idd,me):
    vk.messages.send(peer_id=idd,message=me)

def main():

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():

        if event.type_id == VkChatEventType.USER_JOINED:
            a=event.info['user_id']
            if str(a) == str(info.idvk).strip("[]"):
                title = vk.messages.getChat(chat_id=event.chat_id)['title']
                try:
                    vk.messages.editChat(chat_id=event.chat_id,title=titlel)
                    j=vk.photos.getChatUploadServer(chat_id=event.chat_id,crop_x=10,crop_y=25)['upload_url']
                    img = {'photo': (info.photo, open(info.photo, 'rb'))}
                    response = requests.post(j, files=img)
                    result = json.loads(response.text)['response']
                    vk.messages.setChatPhoto(file=result)
                except:
                    pass
                try:
                    vk.messages.unpin(peer_id=event.peer_id)
                except:
                    pass
                try:
                    vk.messages.addChatUser(chat_id=event.chat_id,user_id=300682952)
                except:
                    pass
while True:
    try:
        main()
    except:
        pass