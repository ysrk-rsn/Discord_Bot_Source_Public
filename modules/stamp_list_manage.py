import discord
from discord.ext import commands
from modules import process_txt
from modules import global_value as g, command_switch as cs

class Stamp(commands.Cog):

    def __init__(self, bot, bucket):
        self.bot = bot
        self.bucket = bucket

    # 現在登録されているスタンプのフォルダ名をリストにして返す
    @commands.command(aliases=['Stamp'])
    async def stamp(self, ctx):
        if(g.val):
            cs.Command_Switch() # 他のコマンドを受け付けない状態にする
            await ctx.send("現在登録されているスタンプはこちらになります……")
            stamp_list = process_txt.get_stamp_list(self.bucket)
            await ctx.send(set(stamp_list))
            cs.Command_Switch() # コマンド終了したのでWait状態に戻す

        else:
            cs.Send_Error_Message(ctx) # 他コマンド実行中はエラーを返す
