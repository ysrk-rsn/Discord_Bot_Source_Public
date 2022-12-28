# Discord_Bot_Source_Public
Sample source code of the Discord bot.
The bot has these following skills... (Still developing...)

* Pick up News Topic (Using bs4)
* Get Today's Weather 
* Creating SuperChat Picture (Using Pillow)
* Generate Word Cloud (Using janome, WordCloud)
* Import LINE Stamps (Using bs4)
* Upload a picture to Google-Cloud-Storage (Using google-cloud-storage)
* Auto Talking (Using A3RT)
* Provide you with gossip

# Python Version
3.8.1


# このプロジェクトについて…
ふみふみ（鷺沢文香）に喋らせる【Disocrd Bot】。作成者の遊び場。
現在進行系で拡張中なので、色々とコードが整頓されてなかったりしますがご了承ください、、、（泣）

現在このBotには以下の機能が付いております。
・ニューススクレイピング（Yahoo, Gigazine, Vipper速報）：10個ほどの記事のリンクをEmbedにして投稿
・天気情報の取得：OpenWeatherMapのAPIを利用して全世界の今日の気象情報を取得します（Embed形式）
・スパチャ画像の投稿。ようつべでよく見るアレ。金額設定も出来るし、コメントも付けられます
・ワードクラウドの作成。Twitterでたまに見る発言まとめみたいなやつを作れます。
・LINEスタンプをスクレイピングする。商用ダメ絶対。LINEスタンプは一つ一つに名前を付けることが出来ます。
・画像バックアップ機能。保存した画像をGoogleCloudStorageにアップロードする。自分はふみふみの画像保管庫にしてます。「fumika」と入力すれば画像をランダムに投稿できます。
・自動会話機能。リクルート社が公開している「A3RT」の自動会話APIを使用して簡単な会話が出来ます。OpenAIほどの受け答えは無理。
・トリビアを投稿する機能。GoogleCloudにアップロードしてあるテキストファイルから一つ無駄知識を拾ってきて投稿してくれます。ユーザーがトリビアを追加することも可能です。

