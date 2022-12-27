import discord
import re
import random
import os
import requests
import json
from google.cloud import storage as gcs
from modules import process_txt

LINE_NOTIFY_TOKEN_PATH = './important/line_notify.json'

#カスタム絵文字の送信
async def send_emoji(message, bucket):
    emoji_sercher_regex = re.compile(r'<:(\w*):.*>')
    mo = emoji_sercher_regex.search(message.content)
    if(mo != None):
        shortcut = mo.group(1) # ショートカットの名前
        path = process_txt.search_shortcut(shortcut.lower(), bucket)
        if(path != ""):
            path_regex = re.compile(r'stamps/(.*)')
            mo = path_regex.search(path)
            if(message.author.nick != None):
                text = f"{message.author.nick} がスタンプを送信しました\n" + mo.group(1)

            else:
                text = f"{message.author.name}がスタンプを送信しました\n" + mo.group(1)
            blob = bucket.get_blob(path)
            blob.download_to_filename('./custom.png') #ファイルを一時的にダウンロードする
            await message.channel.send(text, file=discord.File('./custom.png'))
            os.remove('./custom.png') #ファイルを送信後にファイルを消去)

            # ショートカットが一億円スタンプかつmgsからだった場合に対してNotify機能で個人LINEに通知が来る
            if(shortcut == "ichioku" and message.author.id == 676081692632678421):
                with open(LINE_NOTIFY_TOKEN_PATH) as f:
                    data = json.load(f)
                line_notify_token = data["Authorization"]
                line_notify_api = 'https://notify-api.line.me/api/notify'
                headers = {'Authorization': f'Bearer {line_notify_token}'}
                line_message = data["Message"] + '\nサーバー名: ' + message.guild.name + '\nスレッド名: ' + message.channel.name
                data = {'message': f'message: {line_message}'}
                requests.post(line_notify_api, headers = headers, data = data)



#コマンドではなかった場合に検証
async def process_others(message, bucket):
    char_set = message.content.split()
    if(char_set == []):
        return
    nametag = char_set[0].lower()
    stamp_path = 'images/stamps/' + nametag
    stamp_list = bucket.list_blobs(prefix=stamp_path)
    if(list(stamp_list) != []): #empty listではない場合
        if(len(char_set) == 1):
            stamp_list = bucket.list_blobs(prefix=stamp_path)
            stamp_path_list = []
            for i in stamp_list:
                stamp_path_list.append(i.name)

            stamp_image_path = random.choice(stamp_path_list)
            blob = bucket.get_blob(stamp_image_path)
            blob.download_to_filename('./image_from_folder.png') #ファイルを一時的にダウンロードする
            regex = re.compile(r'/.*/(.*/\d+.png)')
            mo = regex.search(stamp_image_path)
            if(message.author.nick != None):
                text = f"{message.author.nick} がスタンプを送信しました\n" + \
                    mo.group(1)

            else:
                text = f"{message.author.name} がスタンプを送信しました\n" + \
                    mo.group(1)
            await message.channel.send(text, file=discord.File('./image_from_folder.png'))
            os.remove('./image_from_folder.png') #ファイルを送信後にファイルを消去

        if(len(char_set) == 2):  # 因数が2つだった場合には1つ目の因数でフォルダにアクセスし、2つ目の引数で画像をサーチして見つかった場合には返信する。
            if(char_set[1].lower() == "list"):  # 2つ目の引数がlistだった場合にスタンプの一覧を返信する
                stamp_list = bucket.list_blobs(prefix=stamp_path)
                stamp_path_list = []
                for i in stamp_list:
                    stamp_path_list.append(i.name)

                if(len(stamp_path_list) <= 40):
                    text = char_set[0] + " のスタンプ一覧を送信します……"
                    await message.channel.send(text)
                    sorted_list = []
                    image_path = 'images/stamps/' + nametag
                    for i in range(len(stamp_path_list)):
                        new_image_path = image_path + '/' + str(i + 1) + '.png'
                        sorted_list.append(new_image_path)

                    regex = re.compile(r'.*/(\d+.png)')
                    for i in range(len(sorted_list)):
                        image_path = sorted_list[i]
                        blob = bucket.get_blob(image_path)
                        blob.download_to_filename('./list_image.png') #ファイルを一時的にダウンロードする
                        mo = regex.search(image_path)
                        await message.channel.send(mo.group(1), file=discord.File('./list_image.png'))
                        
                    os.remove('./list_image.png') #ファイルを送信後にファイルを消去)

                else:
                    await message.channel.send("こちらのフォルダは保存しているスタンプ数が非常に多いです…。サーバーへの負担を考えリストアップは控えるようお願いします……")

            else:  # 2つめの引数をindexとして取得する。
                image_path = char_set[1].lower() + '.png'
                stamp_image_path = stamp_path + '/' + image_path
                blob = bucket.get_blob(stamp_image_path)
                if(blob != None):
                    blob.download_to_filename('./index_image.png') #ファイルを一時的にダウンロードする
                    if(message.author.nick != None): #ニックネームを設定しているか判断
                        text = f"{message.author.nick} がスタンプを送信しました\n" + \
                        nametag + '/' + str(image_path)

                    else:
                        text = f"{message.author.name} がスタンプを送信しました\n" + \
                        nametag + '/' + str(image_path)

                    await message.channel.send(text, file=discord.File('./index_image.png'))
                    os.remove('./index_image.png') #ファイルを送信後にファイルを消去)

    else:  # パスが無ければスタンプショートカットにないかどうかを探す。

        if(len(char_set) == 1):
            path = process_txt.search_shortcut(char_set[0].lower(), bucket)
            if(path != ""):
                path_regex = re.compile(r'stamps/(.*)')
                mo = path_regex.search(path)
                if(message.author.nick != None):
                    text = f"{message.author.nick} がスタンプを送信しました\n" + mo.group(1)

                else:
                    text = f"{message.author.name} がスタンプを送信しました\n" + mo.group(1)
                blob = bucket.get_blob(path)
                blob.download_to_filename('./shortcut_temp.png') #ファイルを一時的にダウンロードする
                await message.channel.send(text, file=discord.File('./shortcut_temp.png'))
                os.remove('./shortcut_temp.png') #ファイルを送信後にファイルを消去)