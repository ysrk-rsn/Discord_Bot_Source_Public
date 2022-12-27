"""
    自動会話APIを使って会話をする機能
"""

import requests
import json
TALK_API_KEY_PATH = './important/a3rt_api.json'

def talk_api(message):
    with open(TALK_API_KEY_PATH) as f:
        data = json.load(f)

    apikey = data["API_KEY"] 
    talk_url = data["END_POINT"]
    payload = {"apikey": apikey, "query": message}
    response = requests.post(talk_url, data=payload)
    try:
        text = response.json()["results"][0]["reply"]
        text = text.translate(str.maketrans({'?': '…?', '。': '…。'})) + '…' # 文香っぽい言い方に変換する
        return text
    except:
        #print(response.json())
        return ""

if __name__ == "__main__":
    print("実験開始！")
    message = "今日のご飯は？"
    replyText = talk_api(message)
    print(replyText)
