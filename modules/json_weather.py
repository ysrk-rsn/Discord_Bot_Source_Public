"""
JSON ファイルを読み込んで任意の場所の天気情報を取得するプログラム
"""

import json
import requests
import pandas as pd
import re

# API Key:
APP_ID = '8132b305530d7b0a086b62898a4b6a82'

#英語表記かどうかの判断
def isalphabet(s):
    alReg = re.compile(r'^[a-zA-Z]+$')
    return alReg.match(s) is not None

#天気のアイコンの取得
def icon_search(weather):

    df = pd.read_csv('./weather_icon.csv', encoding="cp932")

    match = df[df['Name'] == weather]
    if(len(match) == 0):
        return "http://openweathermap.org/img/wn/02d@2x.png"

    else:
        return match.iloc[0, 1]


#JSONでOpenWeathermapから天気情報を取得する（世界の天気に対応）
def get_wheather_JSON(city):

    url = 'http://api.openweathermap.org/data/2.5/weather?units=metric&q={}&APPID={}'.format(
        city, APP_ID)
    r = requests.get(url)

    if(r.status_code != 200):
        return [] 

    else:
        weather_data = json.loads(r.text)  # 辞書型のデータになって返ってくる
        weather_list = []

        weather_list.append(weather_data['weather'][0]['main'])  # 天気情報基本
        weather_list.append(
            weather_data['weather'][0]['description'])  # 天気詳細を取得
        weather_list.append(str(weather_data['main']['temp']) + "℃")  # 現在の気温
        weather_list.append(
            str(weather_data['main']['temp_min']) + "℃")  # 最低気温
        weather_list.append(
            str(weather_data['main']['temp_max']) + "℃")  # 最高気温
        weather_list.append(str(weather_data['main']['humidity']) + "%")  # 湿度
        weather_list.append(str(weather_data['wind']['speed']) + " m/s")  # 風速

        weather_list.append(icon_search(weather_list[0])) #天気アイコンのURL
        weather_list.append(city) #英語表記された都市の名前

        return weather_list
