"""
    ふみふみの画像たちをGCPに格納するパンドラの箱
"""

import asyncio
import discord
import os
import random
from discord.ext import commands
from modules import global_value as g, command_switch as cs


class Fumika(commands.Cog):
    def __init__(self, bot, client, bucket):
        self.bot = bot
        self.client = client
        self.bucket = bucket 

    @commands.command(aliases=['Fumika'])
    async def fumika(self, ctx):
        if(g.val): # 他のコマンドを実行中でないか確認する
            cs.Command_Switch()
            msg = ctx.message.content.rstrip().lower()

            if(msg == "fumika"): #保存した画像の内の一枚をランダムにチャットに貼る
                blobs = self.client.list_blobs('fumifumi_bot', prefix='images/fumika')
                fumika_list = []
                for blob in blobs:
                    fumika_list.append(blob.name)
                
                fumika_image = random.choice(fumika_list) #ランダムに選択
                blob = self.bucket.get_blob(fumika_image)
                blob.download_to_filename('./fumika_image.jpg') #ファイルのダウンロード
                await ctx.send("私の……写真が欲しいのですか…？恥ずかしいですが、よろしければこちらをどうぞ………", file=discord.File('./fumika_image.jpg'))
                os.remove('./fumika_image.jpg') #ファイルを送信後にファイルを消去

            elif(msg == "fumika add"): # 新規の画像を追加する
                await ctx.send("私の写真フォルダに追加する画像を送信して下さい………")

                def check(m):
                    return m.author == ctx.author

                try:
                    reply = await self.bot.wait_for("message", check=check, timeout=40.0)

                except asyncio.TimeoutError:
                    await ctx.send("タイムアウトしました")

                if(len(reply.attachments) == 0):
                    await ctx.send("ファイルが正常に取得できませんでした………")
                
                elif(len(reply.attachments) > 5):
                    await ctx.send("申し訳ございません……。一度に送信できる最大枚数は５枚までです……")

                else:
                    await ctx.send("画像を追加します……。少々お待ち下さい……")
                    blobs = self.client.list_blobs('fumifumi_bot', prefix='images/fumika')
                    fumika_list = []
                    for blob in blobs:
                        fumika_list.append(blob.name)

                    for i in range(len(reply.attachments)):
                        path = './fumika_add_image.jpg'
                        await reply.attachments[i].save(path)
                        gcs_image_path = 'images/fumika/fumika' + str(len(fumika_list) + 1 + i) + '.jpg'
                        blob = self.bucket.blob(gcs_image_path)
                        blob.upload_from_filename(path)

                    text = "合計" + str(len(reply.attachments)) + "枚の画像を新規追加致しました……"
                    await ctx.send(text)
                    os.remove(path)

            elif(msg == "fumika pop"): #アップロードした画像を削除する
                
                if(ctx.author.id == 396575841250836487): # bot作成者専用コマンド

                    blobs = self.client.list_blobs('fumifumi_bot', prefix='images/fumika')
                    fumika_list = []
                    for blob in blobs:
                            fumika_list.append(blob.name)
                    
                    last_fumika_image_path = 'images/fumika/fumika' + str(len(fumika_list)) + '.jpg'
                    blob = self.bucket.blob(last_fumika_image_path)
                    blob.download_to_filename('./fumika_image.jpg') #ファイルのダウンロード
                    await ctx.send("こちらのファイルをフォルダから削除致しますか？………(yes / no でご回答下さい……)\
                        \n（**※※この操作は取り消すことが出来ません…。今一度、ご確認をお願いいたします※※**）", file=discord.File('./fumika_image.jpg'))

                    def check(m):
                        return m.author == ctx.author

                    try:
                        reply = await self.bot.wait_for("message", check=check, timeout=20.0)

                    except asyncio.TimeoutError:
                        await ctx.send("タイムアウトしました")

                    if(reply.content.lower() == "yes"):
                        blob.delete()
                        await ctx.send("該当ファイルを削除致しました……")
                        os.remove('./fumika_image.jpg') #ファイルを送信後にファイルを消去

                    else:
                        await ctx.send("削除をキャンセル致しました……")
                        os.remove('./fumika_image.jpg') #ファイルを送信後にファイルを消去

                else:
                    await ctx.send("申し訳ありません……。こちらのコマンドは管理者専用となっております……")

            cs.Command_Switch() # コマンドが終了したのでWait状態にする

        else:
            await cs.Send_Error_Message(ctx)
                    