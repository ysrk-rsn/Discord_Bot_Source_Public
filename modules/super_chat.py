"""
    スーパーチャットを送信する機能。金額やコメントは任意。金額がランダムである際の色の割合

    青: 5% (1 ~ 5)
    水色: 15% (6 ~20)
    黄緑: 25% (21 ~ 45)
    黄色: 25% (46 ~ 70) 
    オレンジ:15% (71 ~ 85)
    マゼンタ: 10% (86 ~ 95)
    赤: 5% (96 ~ 100)
"""

import discord
from discord.ext import commands
import os
import requests
import json
import textwrap
import random 
from PIL import Image, ImageDraw, ImageFont
from modules import global_value as g, command_switch as cs

PROFILE_LENGTH = 60 # 切り抜きをした際のProfile画像のサイズ
SC_WIDTH = 500 # SC枠の横幅
UPPER_HEIGHT = 80 # プロフィールや金額を乗せる場所の高さ
COMMENT_HEIGHT = 45 #スパチャコメントの行ごとの長さ(pixel)
SPACING = 20 # スパチャコメントの行間

filePath = './prof.jpg'
alphaPath = './profAlpha.png'
resizedPath = './resized.png'
baseImagePath = './base.png'
superChatPath = './superChat.png'

class Super_Chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['superchat', 'Sc', 'SC'])
    async def sc(self, ctx):
        if(g.val):
            # プロフィール画像の加工を行う（円形に抽出する）
            cs.Command_Switch()
            await Modify_Profile_Image(ctx)
            await Create_Super_Chat(ctx)
            cs.Command_Switch()

        else:
            await cs.Send_Error_Message(ctx)

# 以下、スパチャ画像の出力準備
# コマンド入力者のプロフィール画像を切り抜く
async def Modify_Profile_Image(ctx):

    # コマンド送信者のプロフィール画像をダウンロードする
    response = requests.get(ctx.author.display_avatar)
    image = response.content

    with open(filePath, "wb") as dlFile:
        dlFile.write(image)

    # 保存したイメージを読み込む -> 正方形にクリッピングする(中心から短い方の縦横の大きさの正方形)
    im_rgb = Image.open(filePath)
    if (im_rgb.width < im_rgb.height):
        clip_length = im_rgb.width
    else:
        clip_length = im_rgb.height
    
    #中心から任意の正方形にくり抜く
    im_rgb_square = im_rgb.crop(((im_rgb.width - clip_length) // 2,
                        (im_rgb.height - clip_length) // 2,
                        (im_rgb.width + clip_length) // 2,
                        (im_rgb.height + clip_length) // 2))

    # クリッピング用の画像の準備(円形)
    im_a = Image.new("L", im_rgb_square.size, 0)
    draw = ImageDraw.Draw(im_a)
    draw.ellipse((0, 0, clip_length, clip_length), fill=255) #(左下のX座標, 左下のY座標, 右上のX座標, 右上のY座標)

    # 円形の図形にアルファチャンネルを設定してくり抜いたものを保存する
    im_rgba = im_rgb_square.copy()
    im_rgba.putalpha(im_a)
    im_rgba_crop = im_rgba.crop((0, 0, clip_length, clip_length))
    #im_rgba_crop.save(alphaPath)

    # 任意の直径になるようにリサイズする
    resized = im_rgba_crop.resize((PROFILE_LENGTH, PROFILE_LENGTH))
    # await ctx.send("リサイズに成功しました")
    resized.save(resizedPath)

    # await ctx.send(file=discord.File(resizedPath)) #テスト送信

# SuperChat画像の作成開始
async def Create_Super_Chat(ctx):
    #print("sc作成開始")

    #コメントの再調整
    char_list = ctx.message.content.split()
    #print(char_list)

    # スパチャの色一覧をまとめたJSONファイルを開く
    with open('./color_list.json') as f:
        data = json.load(f)

    # コマンドの長さが1以上だった場合の処理
    if(len(char_list) > 1):
        
        # リストの２つめの単語が数値のみだった場合にそれをSuperChatの金額として処理する。その後の単語を全てコメントとして処理する
        if(str.isnumeric(char_list[1])):
            SuperChatPrice = int(char_list[1]) #スパチャ金額の設定
            if(len(char_list) > 2):
                originalComment = " ".join(char_list[2:]) # ３つ目以降の単語を全て連結させる
            else:
                originalComment = "" # 金額のみの場合は空白コメントを入れる
        else:
            SuperChatPrice = CreateRandomSuperChatPrice(data) # スパチャ金額をランダムに設定する
            originalComment = " ".join(char_list[1:]) # 2つ目以降の単語を全て連結させる

    else:
        SuperChatPrice = CreateRandomSuperChatPrice(data) # スパチャ金額をランダムに設定する (金額設定を行う関数を作る)
        originalComment = "" # 金額のみの場合は空白コメントを入れる

    #スパチャの金額をカンマ区切りにする
    SuperChatPriceStr = "￥" + '{:,}'.format(SuperChatPrice) 
    #print(SuperChatPriceStr)

    # SCのコメント枠の初期値
    sc_height = UPPER_HEIGHT

    # コメントに改行を入れて調節する  
    wrapList = textwrap.wrap(originalComment, 23)
    #print(wrapList, len(wrapList))
    modifiedComment = ""
    if(len(wrapList) > 0):
        modifiedComment = wrapList[0]

    # 文字列が複数行なら枠の長さ
    if(len(wrapList) > 1): 
        for i in range(1, len(wrapList)):
            modifiedComment += ('\n' + wrapList[i])

    sc_height += COMMENT_HEIGHT * len(wrapList)

    #print(modifiedComment)

    # 金額に応じて色分けを行う。色のID分岐を行う
    if(SuperChatPrice < 200):
        colorID = 0
    elif(SuperChatPrice < 500):
        colorID = 1
    elif(SuperChatPrice < 1000):
        colorID = 2
    elif(SuperChatPrice < 2000):
        colorID = 3
    elif(SuperChatPrice < 5000):
        colorID = 4
    elif(SuperChatPrice < 10000):
        colorID = 5
    else:
        colorID = 6
    
    # スパチャ枠全体の描画
    scImage = Image.new('RGB', (SC_WIDTH, sc_height), (data["Colors"][colorID]["Header_BG"][0],data["Colors"][colorID]["Header_BG"][1],data["Colors"][colorID]["Header_BG"][2],1)) # モード、サイズ(width, height)、塗りつぶす色

    # スパチャ画面を編集する
    draw = ImageDraw.Draw(scImage)

    # フォントの定義を行う
    font_path = './fonts/meiryob.ttc' # Windowsのフォントファイルへのパス
    font_size = 20  # フォントサイズ
    font = ImageFont.truetype(font_path, font_size) 

    # ユーザー名を挿入する
    if(ctx.author.nick != None):
        userName = ctx.author.nick
    else:
        userName = ctx.author.name

    draw.text((UPPER_HEIGHT + SC_WIDTH // 20, UPPER_HEIGHT / 8), userName, 
                        (data["Colors"][colorID]["Header_UserName"][0],data["Colors"][colorID]["Header_UserName"][1],data["Colors"][colorID]["Header_UserName"][2]), font=font) # 文字色も後々変数で処理できるように変更する

    # 金額を挿入する
    draw.text((UPPER_HEIGHT + SC_WIDTH // 20, UPPER_HEIGHT / 2), SuperChatPriceStr ,
                        (data["Colors"][colorID]["Header_Price"][0],data["Colors"][colorID]["Header_Price"][1],data["Colors"][colorID]["Header_Price"][2]), font=font) # 文字色も後々変数で処理できるように変更する

    # コメント(メッセージ)を挿入する
    if(len(modifiedComment) > 0):
        # コメント部分のベースの描画
        #print("コメント処理")
        draw.rectangle((0, UPPER_HEIGHT, 500, sc_height), 
                    fill=(data["Colors"][colorID]["Lower_BG"][0],data["Colors"][colorID]["Lower_BG"][1],data["Colors"][colorID]["Lower_BG"][2])) #drawにおける座標はどうやら左上を(0,0)としているらしい…
        draw.text((SC_WIDTH // 25, UPPER_HEIGHT + 10),  modifiedComment,
                            (data["Colors"][colorID]["Lower_Comment"][0],data["Colors"][colorID]["Lower_Comment"][1],data["Colors"][colorID]["Lower_Comment"][2]), font=font, spacing= SPACING) # 文字色も後々変数で処理できるように変更する

    # 作成したスパチャ画像を保存する
    scImage.save(baseImagePath)
    #await ctx.send("こちらがベースの画像になります", file=discord.File(baseImagePath))

    # スパチャ画像とプロフ画像を合成する
    baseImage = Image.open(baseImagePath)
    profileImage = Image.open(resizedPath)

    superChatImage = baseImage.copy()
    superChatImage.paste(profileImage, (SC_WIDTH // 20, (UPPER_HEIGHT - PROFILE_LENGTH) // 2), profileImage) # 画像と座標を挿入する(３つ目の引数はマスク用)
    superChatImage.save(superChatPath)

    # スパチャを送信して、作成に使った画像情報を削除する
    if(ctx.message.author.nick != None):
        text = f"{ctx.message.author.nick} がSuperChatを送信しました"

    else:
        text = f"{ctx.message.author.name} がSuperChatを送信しました"
    # await ctx.message.delete() # コマンドを削除

    # スパチャ画像を送信する＆作成に使用した画像の削除
    await ctx.send(text, file=discord.File(superChatPath))
    os.remove(filePath)
    os.remove(resizedPath)
    os.remove(baseImagePath)
    os.remove(superChatPath)


# スパチャ金額の設定
def CreateRandomSuperChatPrice(data):
    #print("SuperChatの金額を設定します")

    # 色の乱数を決定する
    #青: 5% (1 ~ 5) 水色: 15% (6 ~20) 黄緑: 25% (21 ~ 45) 黄色: 25% (46 ~ 70)  オレンジ:15% (71 ~ 85) マゼンタ: 10% (86 ~ 95) 赤: 5% (96 ~ 100)
    colorRand = random.randint(1,100)
    colorID = 0
    if(colorRand < 6):
        colorID = 0
    elif(colorRand < 21):
        colorID = 1
    elif(colorRand < 46):
        colorID = 2
    elif(colorRand < 71):
        colorID = 3
    elif(colorRand < 86):
        colorID = 4
    elif(colorRand < 96):
        colorID = 5
    else:
        colorID = 6

    # 乱数を返す(金額の下限値と上限値から乱数で算出する)
    return random.randint(data["Colors"][colorID]["Price_Min"], data["Colors"][colorID]["Price_Max"])
    
    


        