import requests
import json
from CONFIG import info

your_token=info.token
idgroup=str(info.idvk).strip("[]")
album_id=input('id альбома: ')
count="400"

for x in range(int(count)):
	try:
		h=requests.get("https://api.vk.com/method/photos.get?access_token=%s" % your_token+"&v=5.92&owner_id="+idgroup+"&album_id="+album_id+"&count="+count).json()["response"]["items"][x]["id"]
		print("photo"+idgroup+"_"+str(h))
	except:
		pass