import telebot
import requests
import json
from key import API_KEY

bot = telebot.TeleBot(API_KEY)
API = 'fce82447e26f829b9a3e17cd872aded6'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Добро пожаловать на ПОГОДА.net Бота\n"
                                      "Введи название города, чтобы узнать информацию о погоде!")


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric")
    if response.status_code == 200:
        data = json.loads(response.text)
        temp = data['main']['temp']

        img = ''
        if temp >= 0 and temp < 10:
            img = 'images/suncloud.jpeg'
        elif temp > 10:
            img = 'images/sun.png'
        elif temp < 0 and temp >= -10:
            img = 'images/rain.png'
        elif temp < -11:
            img = 'images/snow.png'
        file = open('./' + img, 'rb')
        text = f"Погода в {data['name']}: {temp} градусов."
        bot.send_photo(message.chat.id, file)
        bot.reply_to(message, text=text)
    else:
        bot.reply_to(message, text="Название города, указанно не верно!!!")


bot.polling(none_stop=True)
