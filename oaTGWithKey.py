import requests
import telegram
from telegram.ext import Updater, MessageHandler, Filters
TOKEN = "Telegramm bot TOKEN"
url = 'https://api.openai.com/v1/chat/completions'
key = "API key"
headers = {'Content-Type': 'application/json', "Authorization": f"Bearer {key}"}
textHistory= []
textHistoryDict = {"model": "gpt-3.5-turbo","messages":textHistory}
def start_gpt(update, context):
    text = update.message.text
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text}]
    }
    print(textHistory)
    textHistory.append({"role": "user", "content": text})
    response = requests.post(url, headers=headers, json=textHistoryDict)
    if response.ok:
        response_data = response.json()
        if 'choices' in response_data and response_data['choices']:
            message = response_data['choices'][0]['message']
            textHistory.append(message)
            # print(message)
            if 'content' in message:
                content = message['content']
                update.message.reply_text(content)
    else:
        update.message.reply_text("Ошибка запроса: {}".format(response.status_code))

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, start_gpt))
    updater.start_polling()

if __name__ == '__main__':
    main()
