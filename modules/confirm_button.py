import discord
from discord.ext import commands
import asyncio

class Confirm_Cheker(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.timeout = 10
        self.ctx = ctx
        self.answer = False # この値でYES/NOを判断する
    
    # 決定処理
    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if(interaction.user == self.ctx.author):
            await interaction.response.send_message('Confirming...')
            self.value = True 
            self.answer = True # この値でYES/NOを判断する
            self.stop()
            await interaction.message.delete()
            
        else:
            await self.ctx.send("コマンド入力者以外は押下しないようにお願いします…")

    # キャンセル処理
    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if(interaction.user == self.ctx.author):
            await interaction.response.send_message('Cancelling...')
            self.value = False
            self.answer = False
            self.stop()
            await interaction.message.delete()        

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
        return self.answer
