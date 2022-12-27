"""
デレマスのアイドルのプロフィールをcsvファイルから読み込む
"""

import pandas as pd

def get_idol_profile(name):
    df = pd.read_csv("./Idol_Profile.csv", encoding="cp932")
    idol_data = df[df['名前'].str.contains(name)]
    return idol_data
