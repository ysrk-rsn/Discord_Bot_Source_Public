"""
本日のお天気を返す。
天気情報の取得に関しては別ファイル「weather.py」にて行われる。
"""
import discord
from modules import weather, json_weather
from discord.ext import commands
from modules import global_value as g, command_switch as cs

def create_tenkiJp_list(city, weather_list):
    text_disc = city + "の本日の気象情報をお伝えします………"
    text_temp = weather_list[3] + " / " + weather_list[4] + \
        ' / ' + weather_list[5] + ' / ' + weather_list[6]
    embed = discord.Embed(title="**本日の天気**", description=text_disc,
                            color=discord.Colour.from_rgb(0, 100, 100))

    #本日の天気からembedのサムネイルを変更するようにする
    embed.set_thumbnail(
        url=weather_list[9])
    embed.add_field(
        name="**天気**", value=weather_list[0], inline=False)
    embed.add_field(name="**最高気温(℃)**", value=weather_list[1])
    embed.add_field(name="**最低気温(℃)**", value=weather_list[2])
    embed.add_field(
        name="**降水確率:\n０～６時 / ６～１２時 / １２～１８時 / １８～２４時**", value=text_temp, inline=False)
    embed.add_field(name="**紫外線**", value=weather_list[7])
    embed.add_field(name="**洗濯物**", value=weather_list[8])
    return embed

def create_openWeather_list(weather_list):
    text_disc = weather_list[8] + "の本日の気象情報をお伝えします………"
    embed = discord.Embed(
        title="**本日の天気**", description=text_disc, color=discord.Colour.from_rgb(0, 100, 100))
    embed.set_thumbnail(
        url=weather_list[7])
    embed.add_field(
        name="**天気**", value=weather_list[0], inline=False)
    embed.add_field(
        name="**詳細**", value=weather_list[1], inline=False)
    embed.add_field(name="**現在の気温**", value=weather_list[2])
    embed.add_field(name="**最低気温**", value=weather_list[3])
    embed.add_field(name="**最高気温**", value=weather_list[4])
    embed.add_field(name="**湿度**", value=weather_list[5])
    embed.add_field(name="**風速**", value=weather_list[6])
    return embed


class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["Weather"])
    async def weather(self, ctx):
        if(g.val):
            cs.Command_Switch() # 他のコマンドを受け付けない状態にする
            char_list = ctx.message.content.split()
            if(len(char_list) > 1):
                city = " ".join(char_list[1:])
                weather_list = json_weather.get_wheather_JSON(city)
                if(weather_list == []):
                    await ctx.send("申し訳有りません。データの取得に失敗しました……")

                else:
                    embed = create_openWeather_list(weather_list)
                    await ctx.send(embed=embed)

            else:
                await ctx.send("引数の数が正しくありません……")

            cs.Command_Switch() # コマンドを終了したのでWait状態に戻す

        else:
            await cs.Send_Error_Message(ctx)