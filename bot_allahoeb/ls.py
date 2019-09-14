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
    key = ImageToTextTask.ImageToTextTask(anticaptcha_key=info.captcha, save_format='const') \
            .captcha_handler(captcha_link=captcha.get_url())
    return captcha.try_again(key['solution']['text'])


vk_session = vk_api.VkApi(token=info.token, captcha_handler=captcha_handler)
vk = vk_session.get_api()

idvk = info.idvk

def main():

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():

        if event.type == VkEventType.MESSAGE_NEW and event.to_me is not event.from_chat and event.user_id > 0 and not event.user_id in idvk:
            sleep(1)
            b=str(event.text)
            if b[0:8] != "https://":
                f = open(info.msgs)
                data = f.read()
                msg = data.split('\n')[random.randint(0,len(open('фразы.txt', 'r').readlines()))]
                vk.messages.setActivity(user_id=event.user_id,type='typing')
                sleep(random.randint(5,10))
                vk.messages.send(user_id=event.user_id,random_id=random.randint(100000,999999),message=msg)
            elif b[0:8] == "https://":
                try:
                    vk.messages.joinChatByInviteLink(link=b)
                except:
                    pass
while True:
    try:
        main()
    except Exception as e:
        pass