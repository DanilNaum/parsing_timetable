import random
import parsing
from privatInfo import token, vk_id
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

listOfChatForMessageEveryDay=[]


def chat_sender(id,message, random_id = random.randrange(1, 2147483645)):
    vk.messages.send(chat_id= id, message= message, random_id= random_id)

def user_sender(id,message):
    vk.messages.send(user_id= id, message= message, random_id= random.randrange(1, 2147483645))

def MessageEveryDay(chat_id,randIdForMessageEveryDay = 0, timeForMessHour = 9, timeForMessMin = 0):
    date = parsing.dt.datetime.now()
    if date.hour == timeForMessHour and date.minute == timeForMessMin:
        chat_sender(chat_id, "текст сообщения", randIdForMessageEveryDay)

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, vk_id)


while True:


    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    id = int(event.chat_id)
                    message_text = event.message['text']
                    if message_text[0] in '/+><':
                        if message_text[1:] == 'start':
                            listOfChatForMessageEveryDay.append(id)
                            chat_sender(id, "Вы подписались на ежедневную рассылку рассписания!")
                    else:
                        print(message_text)
                        chat_sender(id, message_text)
                if event.from_user:
                    id = int(event.message['from_id'])
                    message_text = event.message['text']
                    print(message_text)
                    user_sender(id, message_text)

        except Exception:
            print(Exception)
    else:
        continue