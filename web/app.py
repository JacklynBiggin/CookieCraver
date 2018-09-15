import pymysql
from flask import jsonify, request
# import pymysql.cursors

from flask import Flask
app = Flask(__name__)

connection = None

def connect():
    global connection
    connection = pymysql.connect(host='cookiecravedb.mysql.database.azure.com',
                                 user='cookieadmin@cookiecravedb',
                                 password='CureCancer!',
                                 db='test',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

def disconnect():
    global connection
    connection.commit()
    connection.close()

@app.route('/user', methods=("POST"))
def createUser():
    connect()
    try:
        with connection.cursor() as cursor:
            query = "INSERT INTO `users` (`uid`, `score`) VALUES (%s, 0)"
            cursor.execute(query, request.json["uid"])
            disconnect()
            return jsonify({}), 200
    except Exception:
        return jsonify({}) , 400

@app.route('/user/cookies', methods=("GET"))
def getUserCookies():
    connect()
    try:
        with connection.cursor() as cursor:
            query = "SELECT `score` FROM `users` WHERE `uid`=%s"
            cursor.execute(query, (request.args["uid"]))
            disconnect()
            return jsonify({"score": cursor.fetchone()}), 200
    except Exception:
        disconnect()
        return jsonify({}) , 400


@app.route('/user/update', methods=("PUT"))
def updateUserCookies():
    connect()
    try:
        with connection.cursor() as cursor:
            query1 = "SELECT `score` FROM `users` WHERE `uid`=%s"
            query2 = "UPDATE `users` SET `score`=`%s` WHERE `uid`=`%s`"
            cursor.execute(query1, (request.json["uid"]))
            currScore = cursor.fetchone()
            cursor.execute(query2, (currScore + request.json["new"], request.json["uid"]))
            disconnect()
            return jsonify({}), 200
    except Exception:
        disconnect()
        return jsonify({}) , 400

@app.route('/leaderboard', methods=("GET")) # top 100
def getTopUsersAndScores():
    connect()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM `users` ORDER BY `score` DESC LIMIT 100"
            cursor.execute(query)
            disconnect()
            return jsonify(cursor.fetchall()), 200
    except Exception:
        disconnect()
        return jsonify({}) , 400

if __name__ == '__main__':
   app.run(debug = True)
