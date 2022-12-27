"""
「help」コマンド。
"""

import discord
from discord.ext import commands
from modules import global_value as g, command_switch as cs

class Helps(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Help', 'help'])
    async def ヘルプ(self, ctx):
        if(g.val):
            cs.Command_Switch()
            msg = ctx.message.content.lower().rstrip()

            if(len(msg.split()) > 2):
                await ctx.send("引数の数が正しくありません……こちらのコマンドの引数は２つまでです……")

            else:
                if(msg == "help"):
                    embed = discord.Embed(title="**ふみふみbot コマンド集**", description="私に……出来ることを……お教えいたします……。それぞれの詳細は\"help <コマンド名>\"でご確認下さい……。",
                                        color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    # inlineはデフォルトがTrueになっている
                    embed.add_field(name="**auto**",
                                    value="ONにすることで、私と会話することが出来ます…", inline=False)
                    embed.add_field(name="**fumika**",
                                    value="画像フォルダから…私の写真を……送信します…", inline=False)
                    embed.add_field(
                        name="**import**", value="LINEスタンプをショップのURLから自動ダウンロードするコマンドです……", inline=False)
                    embed.add_field(
                        name="**shortcut**", value="ダウンロードしたスタンプのショートカットコマンドを作成します。", inline=False)
                    embed.add_field(name="**emoji**",
                                    value="""ショートカットに登録されているスタンプをカスタム絵文字に登録します……""", inline=False)
                    embed.add_field(name="**stamp**",
                                    value="現在登録されているスタンプのリストを一覧にして送信します………", inline=False)
                    embed.add_field(
                        name="**news**", value="世間で話題になっているニュースのトップ記事の一覧を表示します………", inline=False)
                    embed.add_field(
                        name="**weather**", value="本日の天候を表示します……", inline=False)
                    embed.add_field(name="**profile**",
                                    value="アイドルのプロフィール情報を表示します……", inline=False)
                    embed.add_field(name="**gossip**",
                                    value="ムダ知識を提供します……（こちらのコマンドは\"ゴシップ\",\"hint\", \"ヒント\"といった入力にも対応しております……）", inline=False)
                    embed.add_field(name="**sc**",
                                    value="スーパーチャットを送信します……。お金が無い時に投げ銭をした気分になれます…", inline=False)
                    embed.add_field(name="**wc**",
                                    value="ワードクラウドを使用して過去の発言傾向を調べることが出来ます…。", inline=False)
                    embed.add_field(
                        name="**help**", value="現在表示されているこのガイドラインを表示します…。新機能が追加される度にこちらに書き足していきます……", inline=False)
                    await ctx.send(embed=embed)  # Embedとしてメッセージを送信する

                elif(msg == "help auto"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **auto**\n自動会話モードに移行します", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(name="**auto**",
                                    value="自動返答モードのON/OFFスイッチです。ONの時、私がお話相手になります…。至らぬ点がございましたら申し訳ありません…。", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help fumika"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **fumika**\n私の写真を……取り扱うコマンドになります……（恥ずかしいです…）", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(name="**fumika**",
                                    value="私の写真をフォルダの中からランダムに一枚選んで送信します……", inline=False)
                    embed.add_field(
                        name="**fumika add**", value="私の写真フォルダに新たに画像を追加します……一度に最大５枚までです……", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help import"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **import**\n任意のLINEスタンプを登録します……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(name="**import**", value="最初のレスポンスでスタンプショップのURLをペーストして、次のレスポンスでファイル名を入力して下さい……。\
                        また既存のフォルダ名を入力された場合には自動でスタンプを追加することも可能です。\"stamp\"コマンドを利用して現在登録されているスタンプのフォルダや種類をご確認下さい……", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help shortcut"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **shortcut**\n登録したLINEスタンプにショートカット名を追加します……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(name="**shortcut <フォルダ名> <スタンプ番号>**",
                                    value="ショートカットを新たに登録します……。ガイドラインに従ってショートカット名を自由に設定なさって下さい。\nまた登録完了後にはカスタム絵文字の登録も同時に行うことも出来ます。", inline=False)
                    embed.add_field(name="**shortcut change <ショートカット名>**",
                                    value="既存のショートカット名を変更します。（後のアップデートで変更したショートカットがカスタム絵文字に使われている場合にそちらの方も合わせて変更する機能を搭載させる予定です……）", inline=False)
                    embed.add_field(name="**shortcut remove <ショートカット名>**",
                                    value="登録されているショートカットを削除します…。再登録はもちろん可能です。", inline=False)
                    embed.add_field(name="**shortcut list**",
                                    value="現在登録されているショートカットの一覧を表示します……。（こちらも近日アップデート予定。フォルダごとにショートカット名を分割できるようなシステムを考案中）", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help emoji"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **emoji**\nショートカットに登録したスタンプをカスタム絵文字に登録します……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(name="**emoji <ショートカット名>**", value="""該当スタンプを新たにカスタム絵文字に登録します……。カスタム絵文字は**英数字のみ**有効です。\
                                            それ以外の文字が含まれるショートカットをカスタム絵文字に登録されたい場合はショートカット名の変更を行って下さい……(コマンド: shortcut change <ショートカット名>)""", inline=False)
                    embed.add_field(
                        name="**emoji list**", value="現在このサーバーに登録されているカスタム絵文字の名前リストを表示します…。またカスタム絵文字は通常各サーバーに５０個まで登録することが出来ます…。今現在の残り登録枠数も合わせてお教えいたします……。", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help stamp"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **stamp**\n現在登録されているスタンプ情報を表示します……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(
                        name="**stamp**", value="現在登録されているスタンプのフォルダ名の一覧を表示します……", inline=False)
                    embed.add_field(name="**<フォルダ名> list**",
                                    value="フォルダ内のスタンプを全て表示します。ご参考になさって下さい……", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help news"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **news**\n世間で話題になっているニュースをお伝えします……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(name="**news または news yahoo**",
                                    value="Yahooニュースのトップ記事を表示します……", inline=False)
                    embed.add_field(name="**news gigazine**",
                                    value="Gigazineニュースの最新記事１０個を表示します", inline=False)
                    embed.add_field(name="**news lovelive**",
                                    value="ラブライブの最新SS１０個を表示します", inline=False)
                    embed.add_field(name="**news vipper**",
                                    value="『VIPPERな俺』の最新スレ１０個を表示します", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help weather"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **weather**\n本日の天候をお伝えします……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(
                        name="**weather <都市名>**", value="OpenWeathermapというサイトから本日の天気情報を表示します。日本語入力の際は「市」、「区」まで忘れないようにお願いします……", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help profile"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **profile**\nアイドル達のプロフィールを表示します……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(name="**profile <アイドル名>**",
                                    value="""アイドルのプロフィール情報を表示します。アイドルの名前はフルネームでなくても大丈夫です…。\
                                        しかし、複数の検索結果を伴うような検索文字の場合Pさんが欲しい情報を提供できない可能性がございます……。\n
                                        現在はアイドルマスターシリーズの女性キャラクター達とAqoursの皆さんのデータを保有しています。""", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help gossip"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **gossip **\nトリビアを一つお教えします……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(
                        name="**gossip**", value="日常生活において何の役にも立たないムダ知識をゴシップストーンが提供します…。真偽はPさんにおまかせします……。しかし中には隠しコマンドのヒントになるような噂話もあるかもしれません……。",
                        inline=False)
                    embed.add_field(
                        name="**gossip add**", value="皆様の手でゴシップを追加することが出来ます……。どんなジャンルでも構いませんが、出来る限り内容はトリビアに近いものを追加していただけると幸いです……。",
                        inline=False)
                    embed.set_footer(text="**\n【重要】\"gossip add\"コマンドにおいて入力ミスや削除依頼が生じた場合はBot製作者にご連絡下さい**")
                    await ctx.send(embed=embed)

                elif(msg == "help sc"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **sc**\nスーパーチャットを送信します……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(name="**sc <金額> <メッセージコメント>**",
                                    value="""スーパーチャットを送信することが出来ます…。金額とメッセージコメントは任意の入力です…。[sc]と入力していただくだけでも送信することが出来ます…。その際金額は乱数で決まります…。""", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help wc"):

                    embed = discord.Embed(
                        title="**ふみふみbot コマンド集**", description="コマンド名: **sc**\nスーパーチャットを送信します……", color=0x0080ff)
                    embed.set_thumbnail(
                        url="https://stickershop.line-scdn.net/stickershop/v1/sticker/240346247/android/sticker.png")
                    embed.add_field(name="**wc**",
                                    value="""過去の発言を一枚の画像にまとめます……。サンプルデータにはこちらのコマンドを入力したスレッドの過去発言5000個を対象とします…""", inline=False)
                    await ctx.send(embed=embed)

                elif(msg == "help help"):

                    text = f"{ctx.message.author.mention}\nFrom bot　製作者：わざわざこのようなコマンドを入力するそのデバッグ精神。嫌いじゃないが、君のような人がいると無駄に作業量が増えそうなので勘弁して下さい（）"

                    await ctx.send(text)
                    await ctx.send("隠しコマンド(難易度１)")

                elif(msg == "help me"):

                    embed=discord.Embed(title="**Help me, ERINNNNNN!!**", url="https://www.nicovideo.jp/watch/sm3470236", description="**助けてえーりん！！**", color=0x0000ff)
                    embed.set_thumbnail(url="https://c-sf.smule.com/rs-s92/arr/9e/ab/a0436f79-2975-43f2-b0bc-bf6accf9e766.jpg")
                    embed.add_field(name="(ﾟ∀ﾟ)o彡゜えーりん！えーりん！", value="(ﾟ∀ﾟ)o彡゜えーりん！えーりん！", inline=False)
                    embed.add_field(name="(ﾟ∀ﾟ)o彡゜りんえー！りんえー！", value="(ﾟ∀ﾟ)o彡゜りんえー！りんえー！", inline=False)
                    embed.set_footer(text="このネタ分かる人いるーー？？")
                    await ctx.send(embed=embed)
                    await ctx.send(f"{ctx.message.author.mention} 隠しコマンド（難易度３）よくぞ見つけた！")

            cs.Command_Switch()
        
        else:
            await cs.Send_Error_Message(ctx)