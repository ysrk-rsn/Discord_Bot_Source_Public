"""
    WEB解析を行ってLINEスタンプストアからスタンプのリンクのみをスクレイピングする→その後Google Cloud Storageに画像ファイルを保存する
"""

import requests
import bs4
import os
import re
from google.cloud import storage as gcs


def scraping(url, name):

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]='./master.json' 

    client = gcs.Client('fumika')
    bucket = client.get_bucket('fumifumi_bot')
    res = requests.get(url)  # URLからHTMLのデータを取得する
    res.raise_for_status()

    # beautifulsoup4 にDLしたHTMLを登録
    soup = bs4.BeautifulSoup(res.text, "lxml")
    # <li> タグの中にあって、<div>,<span>タグの連続ファイルの直下に入っている要素を全て取得する
    elem = soup.select("li div > span")

    # スタンプのhtmlリンクが表示されているリンク部分のみを抽出するregexオブジェクト
    stamp_regex = re.compile(r'http.*\.png')
    stamp_links = []

    for i in range(len(elem)):  # タグリストの中から
        mo = stamp_regex.search(str(elem[i]))
        if(mo != None):  # マッチするオブジェクトが発見された場合
            if(mo.group() not in stamp_links):
                stamp_links.append(mo.group())

    stamp_links.sort()
    path = 'images/stamps/' + name + '/'

    checkpath = 'images/stamps/' + name
    stamp_list_length = len(list(bucket.list_blobs(prefix=checkpath))) #以前に作成したリストかどうか確認する

    if(stamp_list_length != 0): #以前作成したことのあるリスト
        for i in range(len(stamp_links)):
            r = requests.get(stamp_links[i], stream=True)
            if(r.status_code == 200):
                newpath = path + str(i + 1 + stamp_list_length) + '.png'
                filename = './import_image.png'
                with open(filename, 'wb') as f:
                    f.write(r.content)
                blob = bucket.blob(newpath)
                blob.upload_from_filename('./import_image.png')
                os.remove('./import_image.png') #ファイルを送信後にファイルを消去

    else: #初めて作成するフォルダ名の場合
        for i in range(len(stamp_links)):
            r = requests.get(stamp_links[i], stream=True)
            if(r.status_code == 200):
                newpath = path + str(i + 1) + '.png'
                filename = './import_image.png'
                with open(filename, 'wb') as f:
                    f.write(r.content)
                blob = bucket.blob(newpath)
                blob.upload_from_filename('./import_image.png')
                os.remove('./import_image.png') #ファイルを送信後にファイルを消去

        blob = bucket.get_blob('stamp.txt')
        blob.download_to_filename('./stamp.txt')
        with open('./stamp.txt', 'a', encoding="utf-8-sig") as f:
            # shortcut.txt に書き込む(末尾に追加記入する)
            print(name, file=f)
        blob.upload_from_filename('./stamp.txt')
        os.remove('./stamp.txt')

