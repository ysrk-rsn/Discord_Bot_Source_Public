"""
超重要隠しコマンドはここに定義する
ゴシップで隠しコマンドのヒントや噂を流してくれる。トリビアbotでもある
"""

import discord
from discord.ext import commands
from google.cloud import storage as gcs
import pandas as pd
import random
import os
import asyncio
import datetime as dt
from modules import global_value as g, command_switch as cs

class Gossip(commands.Cog):

    def __init__(self, bot, bucket):
        self.bot = bot
        self.bucket = bucket

    #豆知識を提供
    @commands.command(aliases=[ 'ヒント','hint', 'Hint', 'gossip', 'Gossip']) 
    async def ゴシップ(self, ctx):
        if(g.val):
            cs.Command_Switch()
            msg = ctx.message.content.rstrip().split()
            if(len(msg) == 1): # 何かしらのトリビアを返す
                bucket = self.bucket
                blob = bucket.get_blob('gossipU.txt')
                blob.download_to_filename('./gossipU.txt')
                f = open('./gossipU.txt', 'r', encoding='utf-8-sig')
                lines = f.readlines()
                f.close()

                selectLine = random.randint(1, len(lines))
                count = 1
                for i in lines:
                    count += 1
                    if (count == selectLine):
                        content = i
                        break

                name_tag = "その" + str(selectLine)
                text = "**" + content.rstrip("\n") + "らしい**"
                embed=discord.Embed(title="**ゴシップストーンの噂話**", description="**・・・こっそり聞いた話だが・・・**", color=0xc0c0c0)
                embed.set_thumbnail(url="https://www.nicepng.com/png/full/285-2858456_file-gossip-.png")
                embed.add_field(name=name_tag, value=text, inline=False)
                await ctx.send(embed=embed)
                os.remove('./gossipU.txt')

            #新しくトリビア、ゴシップを追加する（全ユーザーが可能）
            elif(ctx.message.content.lower().rstrip() == "gossip add"):
                await ctx.send("追加する情報をこちらにご入力下さい………")

                def check2(m):
                    return m.author == ctx.author and m.channel == ctx.channel

                try:
                    topic = await self.bot.wait_for("message", check=check2, timeout=120.0)

                except asyncio.TimeoutError:
                    await ctx.send("タイムアウトしました")

                else:
                    bucket = self.bucket
                    blob = bucket.get_blob('gossipU.txt')
                    blob.download_to_filename('./gossipU.txt')
                    with open('./gossipU.txt', 'a', encoding="utf-8-sig") as f:
                        # gossipU.txt の末尾に追加で書き込む
                        print(topic.content.rstrip(), file=f)

                    f = open('./gossipU.txt', 'r', encoding='utf-8-sig')
                    lines = f.readlines()
                    f.close()
                    lastLineNum = len(lines)
                    blob.upload_from_filename('./gossipU.txt')
                        
                    await ctx.send("新しいトリビアがここに誕生しました……。ご協力ありがとうございます……")
                    name_tag = "その" + str(lastLineNum)
                    text = "**" + topic.content.rstrip() + "らしい**"
                    embed=discord.Embed(title="**ゴシップストーンの噂話**", description="**・・・こっそり聞いた話だが・・・**", color=0xc0c0c0)
                    embed.set_thumbnail(url="https://www.nicepng.com/png/full/285-2858456_file-gossip-.png")
                    embed.add_field(name=name_tag, value=text, inline=False)
                    await ctx.send(embed=embed)
                    os.remove('./gossipU.txt')

            #最新のゴシップを削除する（管理者専用コマンド）
            elif(ctx.message.content.lower() == "gossip pop"):
                if(ctx.author.id == 396575841250836487):
                    bucket = self.bucket
                    blob = bucket.get_blob('gossipU.txt')
                    blob.download_to_filename('./gossipU.txt')
                    f = open('./gossipU.txt', 'r', encoding='utf-8-sig')
                    lines = f.readlines()
                    f.close()

                    selectLine = len(lines)
                    count = 1
                    for i in lines:
                        if (count == selectLine): #最終行ゴシップの取得
                            content = i
                            break
                        count += 1

                    name_tag = "その" + str(selectLine)
                    text = "**" + content.rstrip("\n") + "らしい**"
                    embed=discord.Embed(title="**ゴシップストーンの噂話**", description="**・・・こっそり聞いた話だが・・・**", color=0xc0c0c0)
                    embed.set_thumbnail(url="https://www.nicepng.com/png/full/285-2858456_file-gossip-.png")
                    embed.add_field(name=name_tag, value=text, inline=False)
                    await ctx.send(embed=embed)
                    await ctx.send("こちらの投稿を削除しますか？(yes / no でお応え下さい……)\nこのコマンドは取り消しが効きません。今一度ご確認下さいますようお願いします………")

                    def check(m):
                        return m.author == ctx.author

                    try:
                        reply = await self.bot.wait_for("message", check=check, timeout=20.0)

                    except asyncio.TimeoutError:
                        await ctx.send("タイムアウトしました")

                    else:
                        if(reply.content.lower() == "yes"):
                            new_text_set = []
                            count = 1
                            for i in lines:
                                count += 1
                                if count != len(lines):
                                    new_text_set.append(i)  # 一番最後の情報はアペンドしない

                                with open('./gossipU.txt', 'w', encoding='utf-8-sig') as f:
                                    for r in new_text_set:
                                        f.write(r)

                            blob.upload_from_filename('./gossipU.txt')
                            await ctx.send("該当のゴシップを削除しました……")
                            os.remove('./gossipU.txt')

                        else:
                            await ctx.send("削除をキャンセルしました……")
                            os.remove('./gossipU.txt')

                else:
                    await ctx.send("申し訳ありません……。こちらのコマンドは管理者専用となっております……")

            else:
                await ctx.send("申し訳ありません……。そのようなコマンドは現在搭載しておりません……。詳細は\"help gossip\"をご参照下さい……")

            cs.Command_Switch()
    
        else:
            await cs.Send_Error_Message(ctx)

                        

    #隠しコマンド（現在時刻を教えてくれる）
    @commands.command(aliases=["今何時？", "何時？", "何時", "なんじ？"])
    async def 今何時(self, ctx):
        current_time = dt.datetime.utcnow() + dt.timedelta(hours=9) #世界標準時刻から９時間進んでいるのが日本時間
        embed=discord.Embed(title="**ゴシップストーンの定時連絡**", description="ゴシップストーンはシバかれた！", color=0xc0c0c0)
        embed.set_thumbnail(url="https://www.nicepng.com/png/full/285-2858456_file-gossip-.png")
        text = "ただいま " + str(current_time.hour).zfill(2) + ":" + str(current_time.minute).zfill(2) + " です！"
        embed.add_field(name="**ボヨヨヨーン!!**", value=text, inline=False)
        await ctx.send(embed=embed)
        await ctx.send("隠しコマンド(難易度２)")