"""
都市の今日の天気を取得する
"""

import bs4
import requests
import re

#tenki.jpから天気情報を取得する（基本的に日本国内のみにしか対応していない）
def get_weather(r):
    weather_list = []
    soup = bs4.BeautifulSoup(r.text, "lxml")

    today = soup.find(class_="today-weather")  # findを使ってスクレイピング

    weather_list.append(today.p.string)  # 天気を取得(string) index = 0
    temperature_list = today.div.find(class_="date-value-wrap")
    temperature_list = temperature_list.find_all("dd")
    weather_list.append(temperature_list[0].span.string)  # 最高気温 index = 1
    weather_list.append(temperature_list[2].span.string)  # 最低気温 index = 2

    precip = soup.select('tr.rain-probability > td')  # 降水確率の部分の取得
    for i in range(4):
        weather_list.append(precip[i].getText())  # 降水確率 index = 3-6

    # 紫外線と洗濯物の情報を追加する
    telop = soup.select('.telop') # div classの"telop"のみをリストで持ってくる
    weather_list.append(telop[0].getText() + "\n(" + telop[1].getText() + ")")
    weather_list.append(telop[2].getText() + "\n(" + telop[3].getText() + ")")

    icon = soup.select('.today-weather > .weather-wrap > .weather-icon > img')
    icon_regex = re.compile(r'src=\"(.*)\" title')
    mo = icon_regex.search(str(icon))
    weather_list.append(mo.group(1))
    
    return weather_list
