# import csv
import sqlite3
import joblib
import pandas as pd
from random import randint, choice
from flask import Blueprint, render_template
from flask import request, redirect, url_for
# from src import DB_FILEPATH

user_bp = Blueprint('user', __name__)
DB_FILEPATH = "/mnt/d/AI_BootCamp/N3XX/N3XX_Project/project_submit/data/Sools.db"
connect = sqlite3.connect(DB_FILEPATH, check_same_thread=False)
cursor = connect.cursor()
model = joblib.load('src/sools.pkl')


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
    return render_template("menu.html", name=name);

@user_bp.route('/taste')
def getTaste(name):
    # month = request.args["month"]
    # species = request.args["species"]

    # if (month & species):

    # return '흐으음...이것이 당신의 취향이군요...', 200;
    return render_template("guess.html", name=name);

@user_bp.route('/taste', methods=['POST'])
def setRecommend(guest):
    month = request.form["month"]
    species = request.form["species"]

    # get names of sool
    sools = get_sools_dict()
    names = list()
    for sool in sools.values():
        if species in sool["name"]:
            name = sool["name"]
            break;
        names.append(sool["name"])

    # if can't search species in title
    if species not in sool["name"]:
        name = choice(names)

    # predict proof
    recommend = 'Y'
    info = {"soolName" : name,  "thumb_count" : randint(5, 19),
        "is_recommend" : recommend, "month" : month}
    df_dict = pd.DataFrame.from_dict([info])
    res = model.predict(df_dict)[0]

    # 예측한 도수에서 적정 범위 내의 술을 찾아 추천
    while True:
        sool = choice(list(sools.items()))[1];
        if ((float(sool["proof"].rstrip('%')) >= float(res - 2))
            & (float(sool["proof"].rstrip('%')) <= float(res + 2))):
            break;
    # sool = choice(list(sools.items()));

    return f'{sool}, 오늘은 이 술과 밤을 함께 하시는거 어떤가요...?', 200;

@user_bp.route('/entire')
def viewAll(name):
    return render_template('list.html', name=name);

if __name__ == "__main__":
    app.run(debug=True);


