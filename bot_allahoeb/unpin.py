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
selfid = info.ignorelist
ignore= info.conflist

def send_message(idd,me):
    vk.messages.send(peer_id=idd,message=me)

def main():

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():

        if event.type_id == VkChatEventType.MESSAGE_PINNED and not int(event.chat_id) in ignore:
            r=vk.messages.getConversationsById(peer_ids=event.peer_id)['items'][0]['last_message_id']
            f=vk.messages.getById(message_ids=r,preview_length='0')['items'][0]['from_id']
            if not int(f) in selfid and int(f) > 0:
                vk.messages.unpin(peer_id=event.peer_id)
while True:
    try:
        main()
    except:
        pass