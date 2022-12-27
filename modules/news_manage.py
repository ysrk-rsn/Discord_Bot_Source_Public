"""
    NEWSをEMBEDにして返す。
    (Ver4.0): newsコマンド単体だった場合にボタンでサイト選択を出来るように改良
"""

import discord
import asyncio
from modules import news
from discord.ext import commands
from modules import global_value as g, command_switch as cs

class News_Cheker(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.timeout = 10
        self.ctx = ctx
        self.answer = False # この値でYES/NOを判断する
        self.news_list = []
    
    # Yahoo News
    @discord.ui.button(label='Yahoo', style=discord.ButtonStyle.blurple)
    async def Yahoo(self, interaction: discord.Interaction, button: discord.ui.Button):
        if(interaction.user == self.ctx.author):
            self.value = True 
            self.answer = True # この値でYES/NOを判断する
            self.stop()
            await interaction.message.delete()
            self.news_list = news.yahoo_news_checker()
            
        else:
            await self.ctx.send("コマンド入力者以外は押下しないようにお願いします…")

    # Gigazine
    @discord.ui.button(label='Gigazine', style=discord.ButtonStyle.green)
    async def Gigazine(self, interaction: discord.Interaction, button: discord.ui.Button):
        if(interaction.user == self.ctx.author):
            self.value = True 
            self.answer = True # この値でYES/NOを判断する
            self.stop()
            await interaction.message.delete()
            self.news_list = news.gigazine_news_checker()
            
        else:
            await self.ctx.send("コマンド入力者以外は押下しないようにお願いします…")

    # Vipper
    @discord.ui.button(label='Vipper', style=discord.ButtonStyle.gray)
    async def Vipper(self, interaction: discord.Interaction, button: discord.ui.Button):
        if(interaction.user == self.ctx.author):
            self.value = True 
            self.answer = True # この値でYES/NOを判断する
            self.stop()
            await interaction.message.delete()
            self.news_list = news.vipper_news_checker()
            
        else:
            await self.ctx.send("コマンド入力者以外は押下しないようにお願いします…")

    # タイムアウトした時の処理
    async def on_timeout(self) -> None:
        self.stop()
        for item in self.children:
            item.disabled = True

        await self.message.edit(view = self)
        #await self.message.channel.send("TIMEOUTしました……")
    
    # YES/NO を返すFunction
    async def get_value(self):
        await asyncio.sleep(3)
        return self.news_list


class News(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['News'])
    async def news(self, ctx):
        if(g.val):
            cs.Command_Switch() # 他のコマンドを受け付けない状態にする

            if(ctx.message.content.lower().strip() == "news"): # newsの単語のみだった場合はボタンで場合分け出来るようにしてあげよう
                view = News_Cheker(ctx)
                view.message = await ctx.send("どちらのNewsを取得しますか？(10秒後にタイムアウトします)", view = view)
                def check(i):
                    return i.user == ctx.author

                try:
                    await self.bot.wait_for("interaction", check=check, timeout=10.0)
                
                except asyncio.TimeoutError:
                    await ctx.send("タイムアウトしました")

                else:
                    news_list = await view.get_value()
                    embed = discord.Embed(title="現在のトップ記事一覧！",
                                            description="今現在話題になっているニュースはこちらです……", color=discord.Colour.from_rgb(100, 100, 0))
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")  # 画像のサムネイル
                    for i in range(len(news_list)):
                        current_dict = news_list[i]
                        embed.add_field(
                            name=current_dict['title'], value=current_dict['link'], inline=False)
                    await ctx.send(embed=embed)

            else:
                char_list = ctx.message.content.split()
                found = False
                if(len(char_list) == 2):
                    news_site = char_list[1]
                    if(news_site == "yahoo"):
                        news_list = news.yahoo_news_checker()
                        embed = discord.Embed(title="Yahoo ニュース現在のトップニュース",
                                                description="今現在話題になっているニュースはこちらです……", color=discord.Colour.from_rgb(100, 100, 0))
                        found = True

                    elif(news_site == "gigazine"): # GIGAZINEの場合
                        news_list = news.gigazine_news_checker()
                        embed = discord.Embed(title="GIGAZINE ニュース現在のトップニュース",
                                                description="今現在話題になっているニュースはこちらです……", color=discord.Colour.from_rgb(100, 100, 0))
                        found = True

                    elif(news_site == "lovelive"): # loveliveの場合
                        news_list = news.lovelive_news_checker()
                        embed = discord.Embed(title="ラブライブ! 新着SS情報",
                                                description="ラブライブの新着SSはこちらです……", color=discord.Colour.from_rgb(100, 100, 0))
                        found = True

                    elif(news_site == "vipper"): # vipperの場合
                        news_list = news.vipper_news_checker()
                        embed = discord.Embed(title="VIPPERな俺 新着スレ情報",
                                                description="VIPPERな俺の新着スレはこちらです……", color=discord.Colour.from_rgb(100, 100, 0))
                        found = True

                    if(found):
                        embed.set_thumbnail(
                            url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")  # 画像のサムネイル
                        for i in range(len(news_list)):
                            current_dict = news_list[i]
                            embed.add_field(
                                name=current_dict['title'], value=current_dict['link'], inline=False)

                        await ctx.send(embed=embed)

                    else:
                        await ctx.send("申し訳ございません……。そちらのサイトには対応しておりません…。詳細は\"help news\"をご参照下さい……")

                else:
                    await ctx.send("引数の数が正しくありません……。詳細は\"help news\"をご参照下さい……")
        
            cs.Command_Switch() # コマンドが終了したので元に戻す

        else:
            await cs.Send_Error_Message(ctx) # 他のコマンド実行中の際はエラーメッセージを返す
