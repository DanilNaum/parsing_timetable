import random
import parsing
from privatInfo import token, vk_id
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

listOfChatForMessageEveryDay= []



def chat_sender(id,message, randomId= -1):
    if randomId==-1:
        randomId = random.randrange(1, 2147483645)
    vk.messages.send(chat_id= id, message= message, random_id= randomId)

def user_sender(id,message):
    vk.messages.send(user_id= id, message= message, random_id= random.randrange(1, 2147483645))

def MessageEveryDay(chat_id,messText='что-то пошло не так',randIdForMessageEveryDay = 0, timeForMessHour = 9, timeForMessMin = 0,test= False):
    date = parsing.dt.datetime.now()
    if test or (date.hour == timeForMessHour and int(date.minute) == int(timeForMessMin)):
        chat_sender(chat_id, messText, randIdForMessageEveryDay)

vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api()

longpoll = VkBotLongPoll(vk_session, vk_id)


while True:
    randIdForMessageEveryDay = int(''.join([i for i in parsing.current_day if i.isdigit()]))
    for chat in listOfChatForMessageEveryDay:

        MessageEveryDay(chat[0], messText= parsing.ParsingTimeTable(), randIdForMessageEveryDay= randIdForMessageEveryDay,timeForMessHour=chat[1],timeForMessMin=chat[2])

    for event in longpoll.listen():
        try:
            if event.type == VkBotEventType.MESSAGE_NEW:
                if event.from_chat:
                    id = int(event.chat_id)
                    message_text = event.message['text']
                    if message_text[0] in '/+><':
                        if message_text[1:] == 'start':

                            chat_sender(id, "Вы подписались на ежедневную рассылку расписания!\nУкажите время расссылки в формате hh:mm")
                            event2 = longpoll.check()
                            if event2[0].type == VkBotEventType.MESSAGE_NEW and event2[0].from_chat and id == int(event2[0].chat_id) and len(event2[0].message['text']) == 5:
                                #нужна доп проверка на то, что введино время
                                message_text2 = event2[0].message['text']
                                listOfChatForMessageEveryDay.append([id, int(message_text2[:2]), int(message_text2[3:])])



                    else:
                        print(message_text)
                        chat_sender(id, message_text)
                if event.from_user:
                    id = int(event.message['from_id'])
                    message_text = event.message['text']
                    print(message_text)
                    user_sender(id, "Я пока не умею ничего((")

        except Exception:
            print(Exception)
        break
    else:
        continue