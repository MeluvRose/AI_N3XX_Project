import pandas as pd
import sqlite3
from datetime import datetime

CONNECT = sqlite3.connect("../data/Sools.db")
CURSOR = CONNECT.cursor()

# make tables
def makeDataFrame(s):
    data = pd.read_sql_query(f"SELECT * FROM {s}", CONNECT);
    return data

def isRecommend(short):
    words = ["추천", "굿"];
    for w in words:
        if w in short:
            return 'Y';
    is_good = [word for word in short if word.startswith('좋')]
    if is_good:
        return 'Y';
    return 'N';

# 포스팅 날짜에서 월수를 가져옴
def getMonth(date):
    month = None;
    try:
        month = date.split('.')[1].lstrip('0')
        month = int(month)
    except:
        month = datetime.today().month

    return month;

def engineer(df):
    data = df.copy()

    # feature engineering
    data["is_recommend"] = data["short"].apply(isRecommend)
    data["month"] = data["date"].apply(getMonth)

    condition = (data["thumb_count"] )

    # drop features
    del_cols = ["date", "title", "short", "id"]
    data.drop(del_cols, axis=1, inplace=True)

    return data;

def preprocessing():
    df_sools = makeDataFrame("Sools")
    df_posts = makeDataFrame("PostSools")

    # add feature
    lst_proof = list()
    for id in df_posts.soolId:
        condition = (df_sools.id == id)
        str_proof = str(df_sools[condition].loc[:,'proof'])
        str_proof = str_proof.split('%')[0].split(' ')[-1]
        if '~' in str_proof:
            str_proof = str_proof.split('~')[1]
        try:
            lst_proof.append(float(str_proof))
        except:
            lst_proof.append(0)

    df_posts.insert(len(df_posts.columns), "proof", lst_proof);
    data_fin = engineer(df_posts)
    data_fin.to_csv("../data/my_data.csv", index=False)

preprocessing();
CONNECT.close();
