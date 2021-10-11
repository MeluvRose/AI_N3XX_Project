import os
import sqlite3
from pymongo import MongoClient
from js-lib import crawling

#MongoDB information
HOST = 'cluster0.ddllv.mongodb.net'
USER = 'jinskim'
PASSWORD = '211010'
DATABASE_NAME = 'myFirstDatabase'
COLLECTION_NAME = ['sools', 'postSools']
MONGO_URI = f"mongodb+srv://{USER}:{PASSWORD}@{HOST}/{DATABASE_NAME}?retryWrites=true&w=majority"
DB_FILENAME = 'Sools.db'
# DB_FILEPATH = os.path.join(os.getcwd(), DB_FILENAME)
DB_FILEPATH = os.path.join('../data/', DB_FILENAME)

def getRDB(connect, cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Sools(
            id VARCHAR(20) NOT NULL PRIMARY KEY,
            name VARCHAR(20),
            image VARCHAR(100),
            intro VARCHAR(100),
            proof REAL
        );
    """);

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS PostSools(
            id INTEGER NOT NULL PRIMARY KEY,
            soolName VARCHAR(20),
            date VARCHAR(20),
            title VARCHAR(100),
            short VARCHAR,
            thumb_count INT,
            soolId VARCHAR(20),
            FOREIGN KEY(soolId) REFERENCES Sools(id)
        );
    """);

def setSools(connect, cursor, collection):
    # Sools : id, name, image, ingredient, intro, proof
    temp = list()

    for e in collection.find():
        temp = [e["product_num"], e["name"], e["image"],
            e["intro"], e["proof"]]
        cursor.execute("""
            INSERT OR IGNORE INTO Sools (id, name, image, intro, proof)
            VALUES (?, ?, ?, ?, ?)
        """, temp)

    connect.commit();

def setPosts(connect, cursor, col_s, col_p):
    # Posts : soolName, date, title, short, thumb_count, soolId
    temp = list()
    dict_id = dict()

    # get list of id of sool
    for s in col_s.find():
        dict_id[s["name"]] = s["product_num"]

    for p in col_p.find():
        temp = [p["name"], p["date"], p["title"],
            p["shorts"], p["thumb_count"]]
        # add foreign key from sools
        if temp[0] in dict_id.keys():
            temp.append(dict_id[temp[0]])
        else:
            continue;

        cursor.execute("""
            INSERT OR IGNORE INTO PostSools (soolName, date, title, short, thumb_count, soolId)
            VALUES (?, ?, ?, ?, ?, ?)
        """, temp)

    connect.commit();


# define obj
client = MongoClient(MONGO_URI)
database = client[DATABASE_NAME]
connect = sqlite3.connect(DB_FILEPATH)
cursor = connect.cursor()
collection_s = database[COLLECTION_NAME[0]]
collection_p = database[COLLECTION_NAME[1]]

# 술 정보 가져오기
sools = crawling.crawlingSools();
# 술의 이름만 가져오기
names = list()
for sool in sools:
    names.append(sool["name"]);
# 술 이름을 이용, 블로그 포스팅 정보 가져오기
posts = crawling.crawlingPosts(names);
# 크롤링에 사용된 브라우저 종료

collection_s.insert_many(sools);
collection_p.insert_many(posts);

getRDB(connect, cursor);
setSools(connect, cursor, collection_s);
setPosts(connect, cursor,
    collection_s, collection_p);

# process terminate
connect.close()
crawling.window_quit();
