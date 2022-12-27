"""
    プロフィール情報を返す
"""

import discord 
from modules import profile
from discord.ext import commands
from modules import global_value as g, command_switch as cs

class Profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # 各キャラクターのプロフィール情報をEmbedにして送信する
    @commands.command(aliases=['Profile'])
    async def profile(self, ctx):
        if(g.val):
            cs.Command_Switch() # 他のコマンドを受け付けない状態にする
            char_list = ctx.message.content.split()
            if(len(char_list) != 2):
                await ctx.send("引数の数が正しくありません……。詳細は\"help profile\"をご参照下さい……")

            else:
                name = char_list[1]
                idol_data = profile.get_idol_profile(name)
                if(idol_data.empty):
                    await ctx.send("そちらのデータは存在しません……。入力ミスがございませんか……？")

                else:
                    embed = discord.Embed(title="**アイドル大百科**",
                                            description="**Pさん……私ので良ければいくらでも教えますよ……**")
                    column_list = idol_data.columns.values
                    for i in range(len(idol_data.columns)):
                        if(i in (0, 1, 3, 4, 7, 8, 9)):
                            embed.add_field(
                                name=column_list[i], value=idol_data.iloc[0, i])

                        else:
                            embed.add_field(
                                name=column_list[i], value=idol_data.iloc[0, i], inline=False)

                    await ctx.send(embed=embed)
            
            cs.Command_Switch() #コマンドが終了したのでWait状態に戻す

        else:
            cs.Send_Error_Message(ctx)
