import MySQLdb
import os
import json
import requests
from flask import jsonify, request, render_template
# import pymysql.cursors
from flask import Flask
static_file = os.path.abspath('CookieCraver/web/static')
template_file = os.path.abspath('CookieCraver/web/template')
app = Flask(__name__, template_folder=template_file, static_folder=static_file)

connection = None

value = 0.1

def connect():
    global connection
    connection = MySQLdb.connect(host='cookiecravedb.mysql.database.azure.com',
                                 user='cookieadmin@cookiecravedb',
                                 password='CureCancer!',
                                 db='test')

def disconnect():
    global connection
    connection.commit()
    connection.close()

@app.route('/')
def index():
    connect()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM `users` ORDER BY `score` DESC LIMIT 100;"
            cursor.execute(query)
            disconnect()
            users = list(cursor.fetchall())
            res_users = []
            for user in users:
                res_users.append([user[0], user[1], user[2], user[3], user[4]])
            return render_template('index.html', users=res_users)
    except Exception as e:
        print(e)
        disconnect()
        return jsonify({}) , 400
    

@app.route('/user', methods=["POST"])
def createUser():
    connect()
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO `users` (`uid`, `fname`, `sname`, `pic`,`score`) VALUES (%s,%s,%s,%s, 0);"
            cursor.execute(query, (request.json["uid"],request.json["fname"],request.json["sname"],request.json["pic"],))
            disconnect()
            return jsonify({}), 200
    except Exception as e:
        return jsonify({}) , 400

@app.route('/user/cookies', methods=["GET"])
def getUserCookies():
    connect()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM `users` WHERE `uid`=%s;"
            query2 = "SELECT * FROM `users` ORDER BY `score` DESC   ;"
            cursor.execute(query, (request.args["uid"],))
            user = cursor.fetchone()
            cursor.execute(query2)
            all_users = cursor.fetchall()
            total = len(all_users)
            rank = [idx+1 for idx,item in enumerate(list(all_users)) if item[0] == int(request.args["uid"])]
            if not rank:
                rank[0] = 0
            disconnect() 
            return jsonify({
                "uid": user[0],
                "fname": user[1],
                "sname": user[2],
                "pic": user[3],
                "score": user[4] if user[4] else 0,
                "total": total,
                "rank" :rank[0]
            }), 200
    except Exception as e:
        print(e)
        disconnect()
        return jsonify({}) , 400

@app.route('/user/value', methods=["GET"])
def getUserCookiesValue():
    connect()
    curr = str(request.args["curr"])
    response = requests.get('https://xecdapi.xe.com/v1/currencies.json/?obsolete=false', auth=('cookiecraver156195662', 'tl9ga7jtpim1cqid2g0kajbmpi'))
    abbrev = [elem["iso"] for elem in dict(response.json())["currencies"]]
    if not curr in abbrev:
        return jsonify({"msg": "invalid curr"}), 400
    try:
        with connection.cursor() as cursor:
            query = "SELECT `score` FROM `users` WHERE `uid`=%s;"
            cursor.execute(query, (request.args["uid"],))
            score = int(cursor.fetchone()[0])
            cadValue = 0.1 * score
            newValue = (requests.get('https://xecdapi.xe.com/v1/convert_from.json/?from=CAD&to=%s&amount=%s' % (curr, str(cadValue)), auth=('cookiecraver156195662', 'tl9ga7jtpim1cqid2g0kajbmpi'))).json()
            disconnect()
            return jsonify({"value": newValue["to"]["mid"]}), 200
    except Exception as e:
        print(e)
        disconnect()
        return jsonify({"msg": str(e)}), 400

@app.route('/user/update', methods=["PUT"])
def updateUserCookies():
    connect()
    try:
        with connection.cursor() as cursor:
            query1 = "SELECT `score` FROM `users` WHERE `uid`=%s;"
            query2 = "UPDATE `users` SET `score`=%s WHERE `uid`=%s;"
            cursor.execute(query1, (request.json["uid"],))
            currScore = int(cursor.fetchone()[0])
            if int(request.json["new"]) > currScore:
                cursor.execute(query2, (int(request.json["new"]), request.json["uid"], ))
            disconnect()
            return jsonify({}), 200
    except Exception as e:
        disconnect()
        return jsonify({}) , 400

@app.route('/leaderboard', methods=["GET"]) # top 100
def getTopUsersAndScores():
    connect()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM `users` ORDER BY `score` DESC LIMIT 100;"
            cursor.execute(query)
            disconnect()
            return jsonify(cursor.fetchall()), 200
    except Exception:
        disconnect()
        return jsonify({}) , 400

if __name__ == '__main__':
   app.run(debug = True)
