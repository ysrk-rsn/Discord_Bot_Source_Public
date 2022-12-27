"""
    コマンドの重複を防ぐ
"""
from modules import global_value as g
from discord.ext import commands

def Initialize_Switch():
    g.val = True
    g.mode = False

def Command_Switch(): # コマンド入力待機状態の切り替え
    if(g.val):
        g.val = False

    else:
        g.val = True

async def Mode_Switch(ctx): # 自動返信モードの切り替え
    if(g.mode):
        g.mode = False
        await ctx.send("自動会話モードが**OFF**になりました")

    else:
        g.mode = True
        await ctx.send("自動会話モードを**ON**に変更しました")

async def Send_Error_Message(ctx):
    await ctx.message.reply("申し訳ありません。他のコマンドを実行中です...。しばらくお待ち下さい...")


class CommandSwitchMaker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # コマンドスイッチを強制的に変更する
    @commands.has_permissions(administrator=True) 
    @commands.command(aliases=['switch'])
    async def ComanndSwitch(self, ctx):
        Command_Switch()
        await ctx.send("コマンドスイッチを強制的に変更しました……")