import paho.mqtt.client as mqtt
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.uix.gridlayout import GridLayout

appid = "0fb6abd182fa3df4608f1eabacf82ff6"# полученный при регистрации на OpenWeatherMap.org. Что-то вроде такого набора букв и цифр: "6d8e495ca73d5bbc1d6bf8ebd52c4123"

import requests


class MqttTestApp(App):
    def publish(self, instance):
        broker_url = "m12.cloudmqtt.com"
        broker_port = 10994
        client = mqtt.Client()
        # client(client_id="", clean_session=True, userdata=None, protocol=MQTTv311, transport="tcp")
        client.connect("m12.cloudmqtt.com", 10994, 60)
        # User = "pfyurjdb"
        # password = "c6smEcHB81_q"
        client.username_pw_set("pfyurjdb", "c6smEcHB81_q")

        client.publish(topic="test/temp", payload="11119999", qos=1, retain=False)
        client.username_pw_set("pfyurjdb", "c6smEcHB81_q")

        client.subscribe("test/temp", qos=0)
        client.publish(topic="test/temp", payload="11119999", qos=1, retain=False)

        client.loop_forever()

    # описываем функцию подключения к серверу
    def connectToMqtt(self, instance):
        pass

    def getWeather(self):
        gl.add_widget(Label(text="request_current_weather(city_id)"))

    def build(self):
        gl = GridLayout(cols=3, padding=10)
        l = Label()

        gl.add_widget(Button(text="Connect and publish", on_press=self.connectToMqtt))
        #  gl.add_widget(Button(text="read led status", on_press=self.getData))
        # gl.add_widget(Label(text="Status"))

        gl.add_widget(Button(text="Get Weather", on_press=self.getWeather()))
        # gl.add_widget(Button(text="X"))
        # gl.add_widget(Button(text="X"))

        return gl




def get_wind_direction(deg):
    l = ['С ','СВ',' В','ЮВ','Ю ','ЮЗ',' З','СЗ']
    for i in range(0,8):
        step = 45.
        min = i*step - 45/2.
        max = i*step + 45/2.
        if i == 0 and deg > 360-45/2.:
            deg = deg - 360
        if deg >= min and deg <= max:
            res = l[i]
            break
    return res

# Проверка наличия в базе информации о нужном населенном пункте
def get_city_id(s_city_name):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': s_city_name, 'type': 'like', 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        cities = ["{} ({})".format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print("city:", cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
    except Exception as e:
        print("Exception (find):", e)
        pass
    assert isinstance(city_id, int)
    return city_id

# Запрос текущей погоды
def request_current_weather(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                     params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])
        print("data:", data)
    except Exception as e:
        print("Exception (weather):", e)
        pass

# Прогноз
def request_forecast(city_id):
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': city_id, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
        data = res.json()
        print('city:', data['city']['name'], data['city']['country'])
        for i in data['list']:
            print( (i['dt_txt'])[:16], '{0:+3.0f}'.format(i['main']['temp']),
                   '{0:2.0f}'.format(i['wind']['speed']) + " м/с",
                   get_wind_direction(i['wind']['deg']),
                   i['weather'][0]['description'] )
    except Exception as e:
        print("Exception (forecast):", e)
        pass

#city_id for Volgograd
city_id = 472757

import sys
if len(sys.argv) == 2:
    s_city_name = sys.argv[1]
    print("city:", s_city_name)
    city_id = get_city_id(s_city_name)
elif len(sys.argv) > 2:
    print('Enter name of city as one argument. For example: Petersburg,RU')
    sys.exit()

request_forecast(city_id)

# if __name__ == "__main__":
#     MqttTestApp().run()
