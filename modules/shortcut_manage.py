"""
ショートカットの処理。ユーザーと直接やり取りする箇所。
裏の処理は"process_txt"で行っている
"""

import discord 
import asyncio
import os
import re
from modules import process_txt
from discord.ext import commands
from modules import confirm_button as cb
from modules import global_value as g, command_switch as cs


COMMAND_LIST = ["fumika", "import", "imports", "emoji", "weather", "profile", "news", "help", "stamp", "gossip", "hint", "sc", "superchat", "ヒント", "shortcut", "switch", "commandswitch"]

def isalnum(s):
        alnumReg = re.compile(r'^[a-zA-Z0-9]+$')
        return alnumReg.match(s) is not None

class Shortcut(commands.Cog):
    def __init__(self, bot, bucket):
        self.bot = bot
        self.bucket = bucket

    @commands.command(aliases=['Shortcut'])
    async def shortcut(self, ctx):
        if(g.val):
            cs.Command_Switch() # 他のコマンドを受け付けない状態にする
            char_list = ctx.message.content.rstrip().split()
            if(len(char_list) == 3): #引数の数が３の場合
                #ショートカットの削除
                if(char_list[1] == "remove"):
                    stamp_image_path = process_txt.search_shortcut(char_list[2], self.bucket)

                    if(stamp_image_path != ""): #ショートカットが存在する場合
                        blob = self.bucket.get_blob(stamp_image_path)
                        blob.download_to_filename('./shortcut_image.png') #ファイルを一時的にダウンロードする
                        await ctx.send(file=discord.File('./shortcut_image.png'))

                        #ver4.0にて新規追加
                        view = cb.Confirm_Cheker(ctx)
                        view.message = await ctx.send("こちらのショートカットを削除します……よろしいですか？(10秒後にタイムアウトします)", view = view)
                        def check(i):
                            return i.user == ctx.author

                        try:
                            await self.bot.wait_for("interaction", check=check, timeout=10.0)

                        except asyncio.TimeoutError:
                            await ctx.send("タイムアウトしました")
                            os.remove('./shortcut_image.png') #ファイルを送信後にファイルを消去)

                        else:
                            ans = await view.get_value()
                            if(ans):
                                text = char_list[2] + "のショートカットを削除します……"
                                await ctx.send(text)

                                # 新しいショートカットをテキストファイルに追加
                                process_txt.remove_shortcut(char_list[2])
                                await ctx.send("設定が終了しました")
                                os.remove('./shortcut_image.png')

                            else:
                                await ctx.send("ショートカットの削除をキャンセルしました")
                                os.remove('./shortcut_image.png')

                    else:
                        await ctx.send("Pさんが入力されたショートカット名は現在登録されておりません……")

                #ショートカットの変更
                elif(char_list[1] == "change"):
                    stamp_image_path = process_txt.search_shortcut(char_list[2], self.bucket)

                    if(stamp_image_path != ""): #ファイルの取得に成功した場合
                        blob = self.bucket.get_blob(stamp_image_path)
                        blob.download_to_filename('./shortcut_image.png') #ファイルを一時的にダウンロードする
                        await ctx.send(file=discord.File('./shortcut_image.png'))
                        await ctx.send("画像の取得に成功しました。新しいショートカットネームを入力して下さい……")

                        def check2(m):
                            return m.author == ctx.author

                        try:
                            shortcut_name = await self.bot.wait_for("message", check=check2, timeout=20.0)

                        except asyncio.TimeoutError:
                            await ctx.send("タイムアウトしました")

                        else:
                            shortcut_list = process_txt.get_shortcut_list(self.bucket)
                            if(shortcut_name.content.lower() in COMMAND_LIST): #コマンド名をショートカット名に使用した場合のエラーメッセージ
                                await ctx.send("**【警告】そちらはコマンド名です。プログラムに支障をきたす恐れがあるのでショートカット名に使わないようにお願いします……**")
                                os.remove('./shortcut_image.png')
                                        
                            elif(shortcut_name.content.lower() in shortcut_list): #既存のショートカット名を登録しようとしている場合
                                await ctx.send("そのショートカット名は既に使われております。大変申し訳ありませんが、もう一度最初からやり直して下さい………")
                                os.remove('./shortcut_image.png')

                            else:
                                text = char_list[2] + "のショートカット名を" + \
                                    shortcut_name.content.lower() + "に変更します………"
                                await ctx.send(text)

                                # 新しいショートカットのセット
                                new_shortcut_set = shortcut_name.content + ' ' + \
                                    stamp_image_path + '\n'  

                                # 新しいショートカットをテキストファイルに追加
                                process_txt.change_shortcut(
                                    char_list[2], new_shortcut_set)
                                await ctx.send("設定が終了しました")
                                os.remove('./shortcut_image.png')
                    
                    else:
                        await ctx.send("Pさんが入力されたショートカット名は現在登録されておりません……")

                #ショートカットの新規登録
                else:
                    stamp_image_path = 'images/stamps/' + \
                        char_list[1] + '/' + char_list[2] + '.png'
                    blob = self.bucket.get_blob(stamp_image_path)
                    if(blob != None):
                        # すでにショートカットリストに登録されている場合エラーメッセージを返す
                        shortcut_tag = process_txt.check_shortcut(stamp_image_path, self.bucket)
                        if(shortcut_tag != ""):
                            await ctx.send("この画像は既にショートカットに登録されています。変更する場合は「shortcut change <現在登録されているショートカット名>」で変更して下さい")
                            text = "現在のショートカット名： " + shortcut_tag
                            await ctx.send(text)

                        else:  # 新しいショートカットの設定だった場合
                            blob.download_to_filename('./shortcut_image.png') #ファイルを一時的にダウンロードする
                            await ctx.send(file=discord.File('./shortcut_image.png'))
                            await ctx.send("画像の取得に成功しました……。ショートカット名はいかが致しますか…？（コマンド名を入力しないようにお願いします……）")

                            def check(m):
                                return m.author == ctx.author


                            try:
                                shortcut_name = await self.bot.wait_for("message", check=check, timeout=20.0)

                            except asyncio.TimeoutError:
                                await ctx.send("タイムアウトしました")
                                os.remove('./shortcut_image.png') #ファイルを送信後にファイルを消去)

                            else:
                                shortcut_list = process_txt.get_shortcut_list(self.bucket)

                                if(shortcut_name.content.lower() in COMMAND_LIST): #コマンド名と同じでないかの確認
                                    await ctx.reply("【警告】そちらはコマンド名です。プログラムに支障をきたす恐れがあるのでショートカット名に使わないようにお願いします……")
                                    os.remove('./shortcut_image.png')
                                            
                                elif(shortcut_name.content.lower() in shortcut_list): #既に同じショートカット名が存在していないか
                                    await ctx.send("そのショートカット名は既に使われております。大変申し訳ありませんが、もう一度最初からやり直して下さい………")
                                    os.remove('./shortcut_image.png')

                                else: #ショートカットの追加＆絵文字登録の確認
                                    text = shortcut_name.content.lower() + "のショートカットを作成しました。以降はこちらの名前を入力することでも画像を送信できます……"
                                    await ctx.send(text, file=discord.File('./shortcut_image.png'))
                                    shortcut_set = shortcut_name.content + ' ' + stamp_image_path
                                    blob = self.bucket.get_blob('shortcut.txt')
                                    blob.download_to_filename('./shortcut.txt')
                                    with open('./shortcut.txt', 'a', encoding="utf-8-sig") as f:
                                        # shortcut.txt の末尾に追加で書き込む
                                        print(shortcut_set, file=f)
                                    blob.upload_from_filename('./shortcut.txt')

                                    #ver4.0にて新規追加
                                    view = cb.Confirm_Cheker(ctx)
                                    view.message = await ctx.send("こちらのショートカットを絵文字に追加しますか？(10秒後にタイムアウトします)", view = view)
                                    def check(i):
                                        return i.user == ctx.author

                                    try:
                                        await self.bot.wait_for("interaction", check=check, timeout=10.0)

                                    except asyncio.TimeoutError:
                                        await ctx.send("タイムアウトしました")
                                        os.remove('./shortcut_image.png') #ファイルを送信後にファイルを消去)

                                    else:
                                        ans = await view.get_value()
                                        if(ans):
                                        #if answer.content.lower().strip() == "yes": #回答が'yes"出会った場合
                                            if(isalnum(shortcut_name.content.lower())):
                                                with open('./shortcut_image.png', 'rb') as fd: #ファイルをバイナリモードで読み込む
                                                    await ctx.guild.create_custom_emoji(name=shortcut_name.content.lower(), image=fd.read()) #カスタム絵文字の追加

                                                await ctx.send("カスタム絵文字の作成に成功しました……")
                                                os.remove('./shortcut_image.png') #ファイルを送信後にファイルを消去)

                                            else: #カスタム絵文字には英数字のみで表記された物しか登録ができないため日本語等はエラーを吐いて変更に誘導させる
                                                await ctx.send("絵文字にはアルファベットと数字で表示されるものしか登録ができません……。登録のためにはショートカット名を変更して下さい……")
                                                os.remove('./shortcut_image.png')

                                        else:
                                            await ctx.send("カスタム絵文字には設定しませんでした")
                                            os.remove('./shortcut_image.png') #ファイルを送信後にファイルを消去)

                    else: #引数ミスが発生している場合に返す（指定の画像ファイルを発見出来なかった場合）
                        await ctx.send("ご指定されたファイルは存在しませんでした………")

            elif(len(char_list) == 2):
                # ショートカットの一覧表示
                if(char_list[1].lower() == "list"):
                    await ctx.send("現在登録されているショートカットをリストにして一覧に表示致します……")
                    shortcut_list = process_txt.get_shortcut_list(self.bucket)
                    await ctx.send(set(shortcut_list))

                # ショートカット一覧をsortする
                elif(char_list[1].lower() == "group"):
                    await ctx.send("ショートカットのグループ化を開始します………")
                    process_txt.sort_shortcut_list(self.bucket)
                    await ctx.send("グループ化が終了しました")

                elif(char_list[1].lower() == "キノコ"):
                    await ctx.send("キノコのご利用は計画的にお願いします……")
                    await ctx.send("隠しコマンド（難易度３）")

                else:
                    await ctx.send("申し訳有りません……そのようなコマンドは搭載しておりません…")

            else:
                await ctx.send("引数の数に誤りがあります……。詳しくはhelpをご参照下さい……")

            cs.Command_Switch() # コマンド終了したのでWait状態に戻す

        else:
            cs.Send_Error_Message(ctx)

