import os
import pip

pip.main(['install', 'telegram'])
import requests
import telegram
from telegram.ext import Updater, MessageHandler, Filters

TOKEN = "Telegramm bot TOKEN"
url = 'https://chatgpt-api.shn.hk/v1/'
headers = {'Content-Type': 'application/json'}


def start_gpt(update, context):
  text = update.message.text
  data = {
    "model": "gpt-3.5-turbo",
    "messages": [{
      "role": "user",
      "content": text
    }]
  }

  response = requests.post(url, headers=headers, json=data)
  if response.ok:
    response_data = response.json()
    if 'choices' in response_data and response_data['choices']:
      message = response_data['choices'][0]['message']
      if 'content' in message:
        content = message['content']
        update.message.reply_text(content)
  else:
    update.message.reply_text("Ошибка запроса: {}".format(
      response.status_code))


def main():
  updater = Updater(TOKEN, use_context=True)
  dp = updater.dispatcher
  dp.add_handler(MessageHandler(Filters.text, start_gpt))
  updater.start_polling()


if __name__ == '__main__':
  main()
