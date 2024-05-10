import os

import asyncio

import aiohttp
from dotenv import load_dotenv
from telebot.async_telebot import AsyncTeleBot

load_dotenv()

bot = AsyncTeleBot(token=os.environ.get('TG_BOT_TOKEN'))


@bot.message_handler(commands=['start'])
async def start(message):
    msg = (f'Привет, {message.from_user.first_name}!\n'
           f'Для того, чтобы добавить уведомление, просто напишите его ниже.')
    await bot.send_message(message.chat.id, msg)


@bot.message_handler(content_types=['text'])
async def new_notification(message):
    url = 'http://localhost:8000/notifications/create/'

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data={
            'chat_id': message.chat.id,
            'text': message.text,
        }) as response:
            try:
                text = await response.text()

                if response.status == 500 or response.status == 400:
                    await bot.send_message(message.chat.id,
                                           'Ошибка, проверьте правильность написания текста уведомления.')
                if response.status == 201:
                    await bot.send_message(message.chat.id, 'Уведомление было успешно добавлено.')

                    text_dict = eval(text)

                    notification_delay = text_dict['time_seconds']
                    notification_text = text_dict['text']

                    await asyncio.sleep(notification_delay)

                    await bot.reply_to(message,
                                       f'Привет, ты просил напомнить: {notification_text}.')
            except Exception as e:
                await bot.send_message(message.chat.id, text=f'Ошибка на стороне сервиса, повторите запрос позже.\n'
                                                             f'Детали: "{e}"')


if __name__ == '__main__':
    asyncio.run(bot.polling())
