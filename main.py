import requests
import datetime
from pprint import pprint
from config import open_weather_token 

def get_weather(city, open_weather_token):

    code_to_smile = { 
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
            f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={open_weather_token}&units=metric'
        )
        data = r.json()
        # pprint(data)

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

        print(f''' 
        *****{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*****
        Погода в городе: {city}
        Температура: {cur_weather}С° {wd}
        Влажность: {humidity}% 
        Давление: {pressure} мм.рт.ст. 
        Ветер: {wind} м/c 
        Восход солнца: {sunrise}
        Закат солнца: {sunset}
        Время всего дня: {leng_of_day}
        ''')

    except Exception as ex:
        print(ex)
        print('проверьте название города!')


def main():
    city = input("Enter city name: ")
    # open_weather_token = input("Enter open weather token: ")
    get_weather(city, open_weather_token)

if __name__ == "__main__":
    main()