import requests
import json

phone=input("Введите номер телефона: ")
passwd=input("Введите пароль: ")

try:
	f=requests.get("https://oauth.vk.com/token?grant_type=password&client_id=2274003&client_secret=hHbZxrka2uZ6jB1inYsH&username=%s" % str(phone) + "&password="+str(passwd))
	print('\nВаш токен: '+str(f.json()["access_token"]))
	print('\nВаш айди: '+str(f.json()["user_id"]))
except:
	if str(f.json()["error_description"]) == "open redirect_uri in browser [5]. Also you can use 2fa_supported param":
		print("\nОтключите на время двойную авторизацию")
	else:
		print('\nВведите правильно пароль')