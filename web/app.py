import MySQLdb
import os
import json
from flask import jsonify, request, render_template
# import pymysql.cursors
from flask import Flask
static_file = os.path.abspath('CookieCraver/web/static')
template_file = os.path.abspath('CookieCraver/web/template')
app = Flask(__name__, template_folder=template_file, static_folder=static_file)

connection = None

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
                res_users.append([user[0], user[1], user[2], user[3], "%04d" % user[4]])
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
            cursor.execute(query, (request.args["uid"],))
            disconnect()
            user = cursor.fetchone()
            return jsonify({
                "uid": user[0],
                "fname": user[1],
                "sname": user[2],
                "pic": user[3],
                "score": user[4] if user[4] else 0 
            }), 200
    except Exception:
        disconnect()
        return jsonify({}) , 400


@app.route('/user/update', methods=["PUT"])
def updateUserCookies():
    connect()
    try:
        with connection.cursor() as cursor:
            query1 = "SELECT `score` FROM `users` WHERE `uid`=%s;"
            query2 = "UPDATE `users` SET `score`=%s WHERE `uid`=%s;"
            cursor.execute(query1, (request.json["uid"],))
            currScore = int(cursor.fetchone()[0])
            cursor.execute(query2, (currScore + int(request.json["new"]), request.json["uid"], ))
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
