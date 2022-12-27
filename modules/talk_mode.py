"""
    自動会話モードを切り替える
"""
from discord.ext import commands
from modules import global_value as g, command_switch as cs


class AutoTalk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Auto'])
    async def auto(self, ctx):
        await cs.Mode_Switch(ctx)