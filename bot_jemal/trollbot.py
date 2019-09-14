# -*- coding: utf8 -*-
import vk_api,random,requests,traceback,glob,time,json
from vk_api.longpoll import VkLongPoll, VkEventType, VkChatEventType
from python3_anticaptcha import ImageToTextTask
from python3_anticaptcha import errors
from CONFIG import info
from threading import Thread

def captcha_handler(captcha):
	key = ImageToTextTask.ImageToTextTask(anticaptcha_key=info.captcha, save_format='const') \
			.captcha_handler(captcha_link=captcha.get_url())
	return captcha.try_again(key['solution']['text'])
vk_session = vk_api.VkApi(token=info.token, captcha_handler=captcha_handler)

vk = vk_session.get_api()

selfid = info.ignorelist
ignore = info.conflist

while True:
	try:
		longpoll = VkLongPoll(vk_session)
		for event in longpoll.listen():
			if event.type_id == VkChatEventType.USER_JOINED:
				class join(Thread):
					def __init__(self,event,vk):
						Thread.__init__(self)
						self.event = event
						self.vk = vk
					def run(self):
						a=event.info['user_id']
						chat_id = event.chat_id
						peer_id = event.peer_id
						if str(a) in str(info.idvk):
							try:
								vk.messages.editChat(chat_id=chat_id,title=random.choice(info.titlel))
								j=vk.photos.getChatUploadServer(chat_id=chat_id,crop_x=10,crop_y=25)['upload_url']
								img = {'photo': (random.choice(info.photo), open(random.choice(info.photo), 'rb'))}
								response = requests.post(j, files=img)
								result = json.loads(response.text)['response']
								vk.messages.setChatPhoto(file=result)
							except:
								pass
							try:
								vk.messages.unpin(peer_id=peer_id)
							except:
								pass
							try:
								vk.messages.addChatUser(chat_id=chat_id,user_id=556099083)
							except:
								pass
				my_thread = join(event,vk)
				my_thread.start()
			if event.type_id == VkChatEventType.MESSAGE_PINNED:
				class pin(Thread):
					def __init__(self,event,vk):
						Thread.__init__(self)
						self.event = event
						self.vk = vk
					def run(self):
						peer_id=event.peer_id
						r=vk.messages.getConversationsById(peer_ids=peer_id)['items'][0]['last_message_id']
						f=vk.messages.getById(message_ids=r,preview_length='0')['items'][0]['from_id']
						if not int(f) in info.idvk and int(f) > 0:
							vk.messages.unpin(peer_id=peer_id)
				my_thread = pin(event,vk)
				my_thread.start()
			if event.type_id == VkChatEventType.PHOTO:
				class photo(Thread):
					def __init__(self,event,vk):
						Thread.__init__(self)
						self.event = event
						self.vk = vk
					def run(self):
						chat_id = event.chat_id
						peer_id = event.peer_id
						r=vk.messages.getConversationsById(peer_ids=peer_id)['items'][0]['last_message_id']
						f=vk.messages.getById(message_ids=r,preview_length='0')['items'][0]['from_id']
						title=vk.messages.getChat(chat_id=chat_id)['title']
						if not int(f) in info.idvk and int(f) > 0 and not event.chat_id in info.conflist:
							a=vk.photos.getChatUploadServer(chat_id=event.chat_id,crop_x=10,crop_y=25)['upload_url']
							img = {'photo': (random.choice(info.photo), open(random.choice(info.photo), 'rb'))}
							response = requests.post(a, files=img)
							result = json.loads(response.text)['response']
							vk.messages.setChatPhoto(file=result)
				my_thread = photo(event,vk)
				my_thread.start()
			if event.type_id == VkChatEventType.TITLE:
				class title(Thread):
					def __init__(self,event,vk):
						Thread.__init__(self)
						self.event = event
						self.vk = vk
					def run(self):
						chat_id = event.chat_id
						peer_id = event.peer_id
						r=vk.messages.getConversationsById(peer_ids=peer_id)['items'][0]['last_message_id']
						f=vk.messages.getById(message_ids=r,preview_length='0')['items'][0]['from_id']
						if not int(f) in info.idvk and int(f) > 0 and not event.chat_id in info.conflist:
							vk.messages.editChat(chat_id=chat_id,title=random.choice(info.titlel))
				my_thread = title(event,vk)
				my_thread.start()
			if event.type == VkEventType.MESSAGE_NEW and not event.user_id in info.idvk:
				class msg(Thread):
					def __init__(self,event,vk):
						Thread.__init__(self)
						self.event = event
						self.vk = vk
					def run(self):
						peer_id = event.peer_id
						user_id = event.user_id
						b=event.text
						c=random.choice([1,2])
						if c == 1 and event.text != '' and event.user_id > 0 and not event.user_id in info.idvk:
							if peer_id > 2000000000 and not peer_id-2000000000 in info.conflist and not event.user_id in info.ignorelist:
								time.sleep(random.randint(1,5))
								f = open(info.msgs)
								data1 = f.read()
								msg = data1.split('\n')[random.randint(0,len(open('фразы.txt', 'r').readlines()))]
								g = open(info.fotki)
								data2 = g.read()
								photo = data2.split('\n')[random.randint(0,len(open('фотки.txt', 'r').readlines()))]
								c = open(info.name)
								data3 = c.read()
								name = data3.split('\n')[random.randint(0,len(open('name.txt', 'r').readlines()))]
								vk.messages.setActivity(peer_id=peer_id,type='typing')
								time.sleep(random.randint(5,10))
								vk.messages.send(peer_id=peer_id,random_id=random.randint(100000,999999),message=random.choice(["[id"+str(user_id)+"|"+name+"], "+msg,msg]),attachment=random.choice([str(photo),'','','','','','','']))
							if peer_id < 2000000000 and user_id > 0:
								if b[0:8] != "https://":
									time.sleep(random.randint(1,5))
									f = open(info.msgs)
									data = f.read()
									msg = data.split('\n')[random.randint(0,len(open('фразы.txt', 'r').readlines()))]
									vk.messages.setActivity(peer_id=peer_id,type='typing')
									g = open(info.fotki)
									data2 = g.read()
									photo = data2.split('\n')[random.randint(0,len(open('фотки.txt', 'r').readlines()))]
									time.sleep(random.randint(5,10))
									vk.messages.send(peer_id=peer_id,random_id=random.randint(100000,999999),message=msg,attachment=random.choice([str(photo),'','','','','','','']))
								if b[0:8] == "https://":
									try:
										vk.messages.joinChatByInviteLink(link=b)
									except:
										pass
						if c == 2 and b[0:8] != "https://" and event.text != '' and event.user_id > 0 and not event.user_id in info.idvk and not peer_id-2000000000 in info.conflist:
							if peer_id > 2000000000 and not event.user_id in info.ignorelist:
								time.sleep(random.randint(1,5))
								a=vk.docs.getMessagesUploadServer(type='audio_message',peer_id=user_id)['upload_url']
								say=random.choice(glob.glob("джемал/*.mp3"))
								img = {'file': ('a.mp3', open(say, 'rb'))}
								response = requests.post(a, files=img)
								result = json.loads(response.text)['file']
								owner=vk.docs.save(file=result)['audio_message']['owner_id']
								document=vk.docs.save(file=result)['audio_message']['id']
								send = 'doc'+str(owner)+'_'+str(document)
								vk.messages.setActivity(peer_id=peer_id,type="audiomessage")
								time.sleep(random.randint(5,10))
								vk.messages.send(random_id=random.randint(100000,999999),attachment=send,peer_id=peer_id)
							if peer_id < 2000000000:
								time.sleep(random.randint(1,5))
								a=vk.docs.getMessagesUploadServer(type='audio_message',peer_id=user_id)['upload_url']
								say=random.choice(glob.glob("джемал/*.mp3"))
								img = {'file': ('a.mp3', open(say, 'rb'))}
								response = requests.post(a, files=img)
								result = json.loads(response.text)['file']
								owner=vk.docs.save(file=result)['audio_message']['owner_id']
								document=vk.docs.save(file=result)['audio_message']['id']
								send = 'doc'+str(owner)+'_'+str(document)
								vk.messages.setActivity(peer_id=peer_id,type="audiomessage")
								time.sleep(random.randint(5,10))
								vk.messages.send(random_id=random.randint(100000,999999),attachment=send,peer_id=peer_id)
				my_thread = msg(event,vk)
				my_thread.start()
	except Exception as e:
		print('Ошибка:\n', traceback.format_exc())
		pass