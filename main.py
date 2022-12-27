import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os
import json
from google.cloud import storage as gcs
from modules import fumifumi, fumika, import_manage, stamp_list_manage, shortcut_manage, emoji_manage, weather, json_weather,news, process_txt, command_switch, \
                        news_manage, super_chat,weather_manage, weather_manage, profile_manage, help_manage, other, gossip_manage, confirm_button, super_chat, word_cloud, auto_talk, talk_mode
from modules import global_value as g, command_switch as cs

# TOKENを記載したファイルのPATH（他の人に教えちゃダメ！）
DISCORD_TOKEN_PATH = './important/discord_token.json'
GOOGLE_TOKEN_PATH = './important/master.json' 

intents = discord.Intents.default()
intents.message_content = True

# ふみふみBotのアクセストークンを読み込む
with open(DISCORD_TOKEN_PATH) as f:
        data = json.load(f)
        
TOKEN = data["TOKEN"]
CLIENT_NAME = data["CLIENT_NAME"]
BUCKET_NAME = data["BUCKET_NAME"]

#Google Cloudにログインする
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_TOKEN_PATH

gclient = gcs.Client(CLIENT_NAME)
bucket = gclient.get_bucket(BUCKET_NAME)

# 接続に必要なオブジェクトを生成
bot = commands.Bot(command_prefix='', intents=intents)  # bot はclientのサブクラス（clientクラスを継承している）

# global_valueの設定(Command_Switchを設定する)
cs.Initialize_Switch()

# 起動時に動作する処理
@bot.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print("ログインしました……\nLogin Name:", bot.user.name)
    print("Log in ID: ", bot.user.id)
    #print(g.val)

    #デフォルトのhelpコマンドの削除
    bot.remove_command('help')

    #Cogをインポートする(コマンド達)
    await bot.add_cog(fumifumi.Fumifumi(bot))
    await bot.add_cog(gossip_manage.Gossip(bot, bucket))
    await bot.add_cog(fumika.Fumika(bot, gclient, bucket))
    
    await bot.add_cog(import_manage.Import(bot, bucket))
    await bot.add_cog(stamp_list_manage.Stamp(bot, bucket))
    await bot.add_cog(shortcut_manage.Shortcut(bot, bucket))
    await bot.add_cog(emoji_manage.Emoji(bot, bucket))
    await bot.add_cog(news_manage.News(bot))
    await bot.add_cog(weather_manage.Weather(bot))
    await bot.add_cog(profile_manage.Profile(bot))
    await bot.add_cog(help_manage.Helps(bot))

    await bot.add_cog(super_chat.Super_Chat(bot)) # ver4.0で追加
    await bot.add_cog(word_cloud.WordCloudMaker(bot)) # ver4.0で追加
    await bot.add_cog(talk_mode.AutoTalk(bot)) # ver4.0で追加
    await bot.add_cog(command_switch.CommandSwitchMaker(bot)) # ver4.0で追加

    await bot.change_presence(activity=discord.Game(name="メンテナンス"))

#コンソールにコマンドエラー文を表示させない
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

# メッセージを受信した時の対応
@bot.event
async def on_message(message):

    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return

    if(g.val): #他のメッセージを処理している間はコマンド等を受け付けない

        if(bot.user in message.mentions): # bot がメンションされた場合の処理（ここを自動会話APIに変更してみよう）
            char_list = message.content.split()
            msg = ''.join(char_list[1:]) # 最初の単語はメンションなので飛ばす
            replyText = auto_talk.talk_api(msg)
            await message.reply(replyText)

        elif(g.mode):
            if not (message.content.split()[0].encode('utf-8').isalnum()): # 最初の単語が英語のみであればコマンドやスタンプの可能性が高いので無視
                replyText = auto_talk.talk_api(message.content)
                if(replyText != ""):
                    await message.channel.send(replyText)

        if "<" in message.content:  # メッセージがカスタムスタンプを含んでいた場合
            await other.send_emoji(message, bucket)

        else: #スタンプのフォルダの名前に無いか探す or ショートカットコマンドの中に存在するかどうか確認する
            await other.process_others(message, bucket)

    #コマンド機能とメッセージ機能を共存させるためのコマンド
    await bot.process_commands(message)

bot.run(TOKEN)