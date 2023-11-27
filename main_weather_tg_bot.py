import requests
import datetime
from config import tg_bot_token, open_weather_token
from aiogram import Bot, types 
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor 


bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start']) # хендлер который отправляет сообщение на команду start
async def start_command(message: types.Message):
    await message.answer('Привет, напиши название города я отправлю погоду по этому городу!!!')

@dp.message_handler() # хендлер реагирующий на последующие сообщений 
async def  get_weather(message: types.Message):
    code_to_smile = {  # 
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Drizzle': 'Дождь \U00002614',
        'Thunderstorm': 'Облачно \U000026A1',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
    }

    try: 
        r = requests.get(
            f'http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric'
        )
        data = r.json() 
        

        city = data['name']
        cur_weather  = data['main']['temp']


        weather_description = data['weather'][0]['main']
        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else: 
            print('Не могу понять что за погода, выгляни в окно!')


        humidity  = data['main']['humidity']
        pressure = data['main']['pressure']
        wind = data['wind']['speed']
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])  
        leng_of_day = sunset - sunrise

        await message.reply(f" *****{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*****\nПогода в городе: {city}\n"
                    f"Температура: {cur_weather}С° {wd}\n"
                    f"Влажность: {humidity}%\n"
                    f"Давление: {pressure} мм.рт.ст.\n"
                    f"Ветер: {wind} м/c \n"
                    f"Восход солнца: {sunrise}\n"
                    f"Закат солнца: {sunset}\n"
                    f"Время всего дня: {leng_of_day}")
    except:
        await message.reply('\U00002620 проверьте название города! \U00002620')

if __name__ == '__main__':
    executor.start_polling(dp)