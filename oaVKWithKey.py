import requests
import vk_api
from vk_api.exceptions import VkApiResponseException
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id

TOKEN = "Токен группы ВКонтакте"
GROUP_ID = "ID группы ВКонтакте"
url = 'https://api.openai.com/v1/chat/completions'
key = "API key"
headers = {'Content-Type': 'application/json', "Authorization": f"Bearer {key}"}

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()

def start_gpt(user_id, text):
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text}]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.ok:
        response_data = response.json()
        if 'choices' in response_data and response_data['choices']:
            message = response_data['choices'][0]['message']
            if 'content' in message:
                content = message['content']
                try:
                    vk.messages.send(
                        peer_id=user_id,
                        random_id=get_random_id(),
                        message=content
                    )
                except VkApiResponseException as e:
                    print(e.error_msg)
    else:
        try:
            vk.messages.send(
                peer_id=user_id,
                random_id=get_random_id(),
                message="Ошибка запроса: {}".format(response.status_code)
            )
        except VkApiResponseException as e:
            print(e.error_msg)

def main():
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.GROUP_JOIN:
            # Присоединяемся к беседе после приглашения
            try:
                vk.messages.join_chat_by_invite_link(invite_link=event.text)
            except VkApiResponseException as e:
                print(e.error_msg)
        elif event.type == VkEventType.MESSAGE_NEW and event.to_me:
            user_id = event.user_id
            text = event.text
            start_gpt(user_id, text)

if __name__ == '__main__':
    main()