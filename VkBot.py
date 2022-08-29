import random

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType



token = "vk1.a.34f-QZXQGzC84WsSD1Zn5MwIX3fr3vFNa4Us6LiuvkfHMZEjQXdDnB_Z5sCulnWTCufpD3_4qxlYjmFNzs9OlaCK7gkN3mucKoy0Vag2CcZ4WPaIISfI6zutfsTcoUtKX05ovsKHfIS9PCoaDlPy3emdx5dad1m_xnXrC-Ncl3jl1-AmuwZfcrCIAzFv-SOR"
def sender(id,message):
    session.method('messages.send',{'chat_id': id, 'message': message, "random_id":random.randrange(1, 2147483645)})

session = vk_api.VkApi(token=token)
vk = session.get_api()

longpoll = VkLongPoll(session)


for event in longpoll.listen():
    try:
        if event.type == VkEventType.MESSAGE_NEW:
            if event.from_chat:
                id = event.chat_id
                request = event.object.message['text']
                print(request)
                sender(id, request)
    except Exception:
        print(Exception)
