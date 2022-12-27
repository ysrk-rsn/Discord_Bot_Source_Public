"""
    特定のテキストチャンネルのワードクラウドを作成して、コマンド入力者の発言傾向を視覚化する。
"""
import discord
from discord.ext import commands
from wordcloud import WordCloud
from janome.tokenizer import Tokenizer
import re
import os
from modules import global_value as g, command_switch as cs

TEXT_FILE_PATH = './severlog.txt'
FONT_PATH = './fonts/ipaexg.ttf'
SAVING_PATH = './wc.png'
WIDTH = 800
HEIGHT = 400
MAX_FONT_SIZE = 100
MIN_FONT_SIZE = 25

# クラウド用のテキストデータとして使用可能かどうか判断する
def Content_Checker(msg):
    return not (msg.content.split()[0].encode('utf-8').isalnum()) and not('<' in msg.content) and not('/' in msg.content) and not('ｗ' in msg.content)

# ワードクラウド用の単語を選定する
def get_word_str(text):
    t = Tokenizer()
    token = t.tokenize(text)
    word_list = []
 
    for line in token:
        tmp = re.split('\t|,', str(line))
        #print(tmp)
        # 名詞のみ対象
        if tmp[1] in ["名詞"]:
            # さらに絞り込み
            if tmp[2] in ["一般", "固有名詞"]:
                word_list.append(tmp[0])

    return " " . join(word_list)

# ワードクラウド画像の作成
def Create_WordCloud():
    # テキストファイルの読み込み
    read_text = open(TEXT_FILE_PATH, encoding="utf-8").read()
    #print(read_text)

    # 文字列取得
    word_str = get_word_str(read_text)

    # 画像作成
    wc = WordCloud(font_path=FONT_PATH, width=WIDTH, height=HEIGHT, max_font_size=MAX_FONT_SIZE, min_font_size=MIN_FONT_SIZE).generate(word_str)
 
    # 画像保存
    wc.to_file(SAVING_PATH)


class WordCloudMaker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Wc, WordCloud'])
    async def wc(self, ctx):
        if(g.val):
            reply = await ctx.reply("過去の発言をまとめてみます。スレッドによっては時間をかなり要する可能性がございます……(過去5000の発言を対象)\nチャンネルの履歴を取得中……")
            text = "" # ワードクラウド用のテキストデータの格納
            count = 0 # 進捗用のデータカウント
            messages = [message async for message in ctx.channel.history(limit=5000)] #None の場合は全て
            #print(len(messages))
            #print(type(messages[0]))

            #コマンド入力されたチャンネルの過去の発言をストックする
            for msg in messages: # テキストチャンネルの発言をトレースする
                if(msg.author == ctx.message.author):
                    if(len(msg.content.split()) > 0):
                        if Content_Checker(msg): # コマンドと絵文字、URLをストックしないようにする
                            text +=  msg.content + '\n'

                # 進捗表示機能
                if(count % 100 == 0):
                    replyText = "過去の発言をまとめてみます……(スレッドによっては時間を要する可能性がございます……)\n" + "(サンプルデータ数: " + str(len(messages)) + ")\n" + \
                                    "進捗: " + str(count) + " / " + str(len(messages)) 
                    await reply.edit(content = replyText)        
                
                count += 1

            replyText = "過去の発言をまとめてみます……(スレッドによっては時間を要する可能性がございます……)\n" + "(サンプルデータ数: " + str(len(messages)) + ")\n" + \
                                    "進捗: " + str(len(messages)) + " / " + str(len(messages)) + "\nデータの抽出が完了しました。これより画像の作成に入ります……。"
            await reply.edit(content=replyText)

            # テキストファイルにデータを書き込む
            with open(TEXT_FILE_PATH, 'w', encoding='utf-8-sig') as f:
                f.write(text)
            f.close()

            #ワードクラウドが作成可能かどうか
            if(text != ""):
                # ワードクラウドを作成
                Create_WordCloud()

                message = f"実行が終了しました……{ctx.author.mention}さんの発言傾向はこちらになります……"
                await ctx.send(message, file=discord.File(SAVING_PATH))
                os.remove(SAVING_PATH)

            else: # 不可だった場合にエラーメッセージに書き換える
                replyText = "過去の発言をまとめてみます……(スレッドによっては時間を要する可能性がございます……)\n" + "(サンプルデータ数: " + str(len(messages)) + ")\n" + \
                                    "進捗: " + str(len(messages)) + " / " + str(len(messages)) + "\n申し訳ありません……。対象データが存在しないため作成不可です……"
            os.remove(TEXT_FILE_PATH)

        else:
            await cs.Send_Error_Message(ctx)

