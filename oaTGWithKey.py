import requests
import telegram
from telegram.ext import Updater, MessageHandler, Filters

key = ""
TOKEN = ""
url = 'https://api.openai.com/v1/chat/completions'
headers = {'Content-Type': 'application/json', "Authorization": f"Bearer {key}"}
textHistory= []
textHistoryDict = {"model": "gpt-3.5-turbo","messages":textHistory}

def start_gpt(update, context):
    text = update.message.text
    bot_username = context.bot.username
    is_group = update.message.chat.type in ['group', 'supergroup']

    if is_group and f'@{bot_username}' not in text:
        return

    if text == '/clear':
        textHistory.clear()
        update.message.reply_text("История сообщений очищена.")
        return

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": text}],
        "temperature": 0.9,
        "max_tokens": 4096,
        "n": 1,
        "stop": ["\n"]
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