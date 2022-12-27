from google.cloud import storage as gcs
import os
import asyncio

# ショートカット名から画像のパスを検索する
def search_shortcut(search_word, bucket):
    client = gcs.Client('fumika')
    bucket = client.get_bucket('fumifumi_bot')
    blob = bucket.get_blob('shortcut.txt')
    blob.download_to_filename('./shortcut.txt')
    stamp_image_path = ""
    f = open('./shortcut.txt', 'r', encoding='utf-8-sig')
    while True:  # ショートカットリストのインデックスの中に入力したワードが存在するかどうか確認
        line = f.readline().split()  # 行を読み込む＆テキストを分解
        if not line:
            break
        else:
            index = line[0]
            if(index == search_word):
                stamp_image_path = line[1]
                break
    f.close()
    asyncio.sleep(2)
    os.remove('./shortcut.txt')

    return stamp_image_path


# ショートカットの検索（パスから）
def check_shortcut(stamp_image_path, bucket):
    blob = bucket.get_blob('shortcut.txt')
    blob.download_to_filename('./shortcut.txt')
    shortcut_tag = ""
    f = open('./shortcut.txt', 'r', encoding='utf-8-sig')
    while True:  # ショートカットリストのインデックスの中に入力したワードが存在するかどうか確認
        line = f.readline().split()  # 行を読み込む＆テキストを分解
        if not line:
            break
        else:
            index = line[1]
            if(index == stamp_image_path):
                shortcut_tag = line[0]
                break
    f.close()
    asyncio.sleep(2)
    os.remove('./shortcut.txt')

    return shortcut_tag


# テキストファイルにショートカットを新しく追加する
def change_shortcut(flag_word, shortcut_set):
    client = gcs.Client('fumika')
    bucket = client.get_bucket('fumifumi_bot')
    blob = bucket.get_blob('shortcut.txt')
    blob.download_to_filename('./shortcut.txt')
    f = open('./shortcut.txt', 'r', encoding='utf-8-sig')
    lines = f.readlines()
    f.close()

    new_text_set = []
    for i in lines:
        if flag_word not in i:
            new_text_set.append(i)  # 前のショートカットの名前を含む列を含まない

        else:
            new_text_set.append(shortcut_set)

        with open('./shortcut.txt', 'w', encoding='utf-8-sig') as f:
            for r in new_text_set:
                f.write(r)

    blob.upload_from_filename('./shortcut.txt')
    os.remove('./shortcut.txt')

#既存のショートカットの削除
def remove_shortcut(flag_word):
    client = gcs.Client('fumika')
    bucket = client.get_bucket('fumifumi_bot')
    blob = bucket.get_blob('shortcut.txt')
    blob.download_to_filename('./shortcut.txt')
    f = open('./shortcut.txt', 'r', encoding='utf-8-sig')
    lines = f.readlines()
    f.close()

    new_text_set = []
    for i in lines:
        if flag_word not in i:
            new_text_set.append(i)  # 前のショートカットの名前を含む列を含まない

        with open('./shortcut.txt', 'w', encoding='utf-8-sig') as f:
            for r in new_text_set:
                f.write(r)

    blob.upload_from_filename('./shortcut.txt')
    os.remove('./shortcut.txt')


# ショートカットをスタンプが格納されているディレクトリ順に並び替える
def sort_shortcut_list(bucket):
    blob = bucket.get_blob('shortcut.txt')
    blob.download_to_filename('./shortcut.txt')
    dictionary_list = []
    f = open('./shortcut.txt', 'r', encoding='utf-8-sig')
    while True:
        line = f.readline().split()
        if not line:
            break
        else:
            dictionary = {'name': line[0], 'path': line[1]}
            dictionary_list.append(dictionary)  # 全てのショートカットデータを辞書型にしてリストに格納する
    f.close()
    sorted_dictionary_list = sorted(
        dictionary_list, key=lambda x: x['path'])  # 辞書のリストをpath基準で並び替え
    with open('./shortcut.txt', 'w', encoding='utf-8-sig') as f:
        for i in range(len(sorted_dictionary_list)):
            temp_dict = sorted_dictionary_list[i]
            name = temp_dict['name']
            path = temp_dict['path']
            text = name + ' ' + path + "\n"
            f.write(text)

    blob.upload_from_filename('./shortcut.txt')
    os.remove('./shortcut.txt')

# ショートカットの一覧を返す
def get_shortcut_list(bucket):
    blob = bucket.get_blob('shortcut.txt')
    blob.download_to_filename('./shortcut.txt')
    shortcut_list = []
    f = open('./shortcut.txt', 'r', encoding='utf-8-sig')
    while True:  # ショートカットリストののインデックスの中に入力したワードが存在するかどうか確認
        line = f.readline().split()  # 行を読み込む＆テキストを分解
        if not line:
            break
        else:
            shortcut_list.append(line[0])
    f.close()
    os.remove('./shortcut.txt')
    return shortcut_list


# スタンプの一覧を返す
def get_stamp_list(bucket):
    client = gcs.Client('fumika')
    bucket = client.get_bucket('fumifumi_bot')
    blob = bucket.get_blob('stamp.txt')
    blob.download_to_filename('./stamp.txt')
    stamp_list = []
    f = open('./stamp.txt', 'r', encoding='utf-8-sig')
    while True:  # ショートカットリストののインデックスの中に入力したワードが存在するかどうか確認
        line = f.readline().split()
        if not line:
            break
        else:
            stamp_list.append(line[0])
    f.close()
    os.remove('./stamp.txt')
    return stamp_list
