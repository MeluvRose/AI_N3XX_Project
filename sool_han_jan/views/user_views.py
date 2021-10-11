# import csv
import sqlite3
import joblib
import os
import pandas as pd
from random import randint, choice
from flask import Blueprint, render_template
from flask import request, redirect, url_for

from sool_han_jan import DB_FILEPATH

user_bp = Blueprint('user', __name__)
# DB_FILEPATH = os.path.join(os.getcwd(), __name__, 'data/Sools.db')
DB_FILEPATH = "sool_han_jan/data/Sools.db";
connect = sqlite3.connect(DB_FILEPATH, check_same_thread=False)
cursor = connect.cursor()
model = joblib.load('project_submit/sools.pkl')


# sqlite(RDB) to list
def get_sools_dict():
    cursor.execute("SELECT * FROM Sools");
    rows = cursor.fetchall();
    headers = ["num_sool", "name", "image", "desc", "proof"]
    sools = dict()

    for idx, r in enumerate(rows):
        sools[f'{idx}']=({headers[0] : r[0], headers[1] : r[1], headers[2] : r[2],
            headers[3] : r[3],  headers[4] : r[4]})

    return sools;

@user_bp.route('/')
def viewMenu(name):
    return render_template("menu.html", user=name);

@user_bp.route('/taste')
def getTaste(name):
    return render_template("guess.html", name=name);

@user_bp.route('/taste', methods=['POST'])
def setRecommend(name):
    # check user's choice
    species = request.form.get("species")
    month = request.form.get("month")
    if species == None:
        species = "막걸리"
    if month == None:
        month = 1

    # get names of sool
    sools = get_sools_dict()
    names = list()
    for sool in sools.values():
        if species in sool["name"]:
            name_sool = sool["name"]
            break;
        names.append(sool["name"])

    # if can't search species in title
    if species not in sool["name"]:
        name_sool = choice(names)

    # predict proof
    recommend = 'Y'
    info = {"soolName" : name_sool,  "thumb_count" : randint(5, 19),
        "is_recommend" : recommend, "month" : month}
    df_dict = pd.DataFrame.from_dict([info])
    res = model.predict(df_dict)[0]

    # 예측한 도수에서 적정 범위 내의 술을 찾아 추천
    while True:
        sool = choice(list(sools.items()))[1];
        proof = sool["proof"].rstrip("%ml");
        if ('%' in proof):
            proof = proof.split('%')[1].strip()
        if ('~' in proof):
            proof = proof.split('~')[1].strip()
        if (float(proof) >= float(res - 2)) & (float(proof) <= float(res + 2)):
            break;

    # # return f'{sool}, 오늘은 이 술과 밤을 함께 하시는거 어떤가요...?', 200;
    return render_template("detail.html", name=name, sool=sool);

@user_bp.route('/entire')
def viewAll(name):
    sools = get_sools_dict()
    sools = list(sools.values())
    return render_template('list.html', name=name, sools=sools);

if __name__ == "__main__":
    app.run(debug=True);


