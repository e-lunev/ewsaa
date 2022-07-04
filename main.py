import random
import re
from pyrogram import Client,filters
from pyrogram.raw.functions.messages import GetBotCallbackAnswer
import easyocr
from captcharocket import redact_stock_img
apps = [{"app_id": '1385646', "api": "f0905605b7f939f62270b1a4d28b08f6"},
        {"app_id": '17749190', "api": "30c146c028fff9928670b3cee9b7602f"}]
app_r = random.choice(apps)
api_id = app_r['app_id']
api_hash = app_r['api']
app = Client("account", api_id, api_hash)
user_notify = 'Lolipop223'
hello = [
    'Ержан приступил к работе', 'Приступаю к работе, милорд', 'Опять работать :(', 'Ррррррррработаем', 'Солнце ещё высоко...'
]
print(random.choice(hello))
with app:
    app.send_message(user_notify,random.choice(hello))
def url_filter(text):
    m_str = str(text)
    if text.chat.username != 'wallet':
        match = re.search("[http|https]://t\.me/((?:tonRocketBot|CryptoBot|wallet))\?(.*)=([C|mc|t].*)\\b", m_str)
        if match:
            return True
        else:
            return False
    else: return False
@app.on_message(lambda c,m: url_filter(m))
def check_message(client, message):
    msg_raw = str(message)
    match = re.search("[http|https]://t\.me/((?:tonRocketBot|CryptoBot|wallet))\?(.*)=([C|mc|t].*)\\b", msg_raw)
    if match:
        print(f'Найден чек в чате: {message.chat.username}')
        app.send_message(user_notify, f'Найден чек в чате: {message.chat.username}')
        bot_nickname = match.groups()[0]
        bot_command = match.groups()[1]
        bot_code = match.groups()[2]
        app.send_message(bot_nickname, f'/{bot_command} {bot_code}')
    else: return
@app.on_message(lambda c,m: True if m.chat.username=="CryptoBot" or m.chat.username=="wallet" else False)
def bot_answer_check(client,message):
    if message.text == 'To activate this check, join channel(s) first.':
        for rows in message.reply_markup.inline_keyboard:
            for button in rows:
                print(button.text)
                if button.text != 'Activate Check':
                    app.join_chat(button.url)
                else:
                    client.request_callback_answer(
                        chat_id=message.chat.id,
                        message_id=message.id,
                        callback_data=button.callback_data
                    )
    if message.caption == 'Enter the characters you see in the image.':
        print('Скачивание каптчи')
        captcha = app.download_media(message,'/captcha/')
        reader = easyocr.Reader(['en'])
        result = reader.readtext(captcha)
        message.reply(result[0][1].replace(' ', ''))
    match = re.search('Receiving (.*)',message.text)
    if match:
        msg = f'Получено: {match.groups()[0]} в CryptoBot'
        print(msg)
        app.send_message(user_notify,msg)
    else:
        match = re.search('Вы получили: (.*)', message.text)
        if match:
            msg = f'Получено: {match.groups()[0]} в wallet'
            print(msg)
            app.send_message(user_notify, msg)
        else: return
@app.on_message(filters.bot)
def capthca(client,message):
    if message.caption == 'Choose the answer corresponding to white numbers:':

        captcha = app.download_media(message, '/captcha/')
        resolve = redact_stock_img('w',captcha)

        for rows in message.reply_markup.inline_keyboard:
            print(resolve)
            for button in rows:
                print(button.text)

                if str(button.text) == resolve:
                    print('Отправка колбек запроса')
                    client.request_callback_answer(
                        chat_id=message.chat.id,
                        message_id=message.id,
                        callback_data=button.callback_data
                    )
                else:
                    continue
    if message.caption == 'Choose the answer corresponding to black numbers:':
        captcha = app.download_media(message, '/captcha/')
        resolve = redact_stock_img('b',captcha)
        for rows in message.reply_markup.inline_keyboard:
            print(resolve)
            for button in rows:
                print(button.text)

                if str(button.text) == resolve:
                    print('Отправка колбек запроса')
                    client.request_callback_answer(
                        chat_id=message.chat.id,
                        message_id=message.id,
                        callback_data=button.callback_data
                    )
                else:
                    continue
app.run()
