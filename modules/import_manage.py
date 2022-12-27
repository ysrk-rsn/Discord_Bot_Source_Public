"""
importコマンド（discord上でのフロント処理）
裏での処理は全て「stamp.py」上で行われる
"""

import discord
import asyncio
import requests
from modules import stamp, process_txt #サブディレクトリ同士のインポートでも親ディレクトリからのパスを入力する必要がある
from discord.ext import commands
from modules import global_value as g, command_switch as cs

command_list = ["fumika", "import", "imports", "emoji", "weather", "profile", "news", "help", "stamp", "gossip", "hint", "sc", "superchat", "ヒント", "shortcut"]


class Import(commands.Cog):
    def __init__(self, bot, bucket):
        self.bot = bot
        self.bucket = bucket

    @commands.command(aliases=['import', "Import"])
    async def imports(self, ctx):
        if(g.val):
            cs.command_switch() # 他のコマンドを受け付けない状態にする
            await ctx.send("登録するスタンプのURL（LINEスタンプショップのページ）を送信して下さい")

            # check function
            def check(m):
                return m.author == ctx.author

            try:  # 返事を待つ replyが内容になる
                url = await self.bot.wait_for("message", check=check, timeout=30.0)

            except asyncio.TimeoutError:  # タイムアウトエラーを返す
                await ctx.send("タイムアウトしました")

            else:  # URLの取得に成功したら返す
                try:
                    r = requests.get(url.content)
                    if(r.status_code == 200):
                        await ctx.send("サイトのアクセスに成功しました……。フォルダ名はいかが致しますか？")

                except:
                        await ctx.send("申し訳ありません……サイトに接続することが出来ませんでした…。今一度URLの確認をお願いいたします……")

                else:

                    # check function
                    def check2(m):
                        return m.author == ctx.author

                    try:
                        name = await self.bot.wait_for("message", check=check2, timeout=40.0)

                    except asyncio.TimeoutError:
                        await ctx.send("タイムアウトしました")

                    else:  # スタンプのファイルの名前の取得に成功したらDL開始
                        shortcut_list = process_txt.get_shortcut_list(self.bucket)

                        if(name.content.lower() not in shortcut_list and name.content.lower() not in command_list):
                            await ctx.send("ダウンロードを開始します……")
                            await ctx.send("ダウンロードには約30秒ほどかかります……")
                            stamp.scraping(url.content, name.content)
                            await ctx.send("ダウンロードが終了しました")

                        elif(name.content.lower() in command_list): #コマンド名と同じでないかの確認
                            await ctx.send("【警告】こちらはコマンド名です。プログラムに支障をきたす恐れがあるのでフォルダ名に使わないようにお願いします……")
                        
                        else: #ショートカット名で使われていないかどうかの確認
                            await ctx.send("申し訳ございません…。その名前は既にスタンプのショートカット名で使われております…。もう一度最初から入力して下さい……")

            cs.Command_Switch() # コマンドが終了したのでWait状態に戻す

        else:
            await cs.Send_Error_Message(ctx)