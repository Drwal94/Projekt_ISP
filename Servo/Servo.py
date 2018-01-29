from flask import Flask, render_template, request, jsonify, redirect, url_for
import mysql.connector
import MySQLdb as sql
from datetime import datetime
import requests
import numpy

app = Flask(__name__)
angle = 0
index = 1
ip_adress = '192.168.0.135'

cnx = sql.connect("localhost", "root", "ksemwetipg", "mydb")
cursor = cnx.cursor()
query = "select * from servo"
cursor.execute(query)
result = cursor.fetchall()

# Getting last index from database
if(not(len(result) == 0)):
    for r in result:
        print r
        angle = r[1]
    index = r[0] + 1
cnx.commit()

cursor.close()
cnx.close()


@app.route('/')
def hello_world():
    return render_template("index.html", ip = ip_adress)

def send_Data(angle_form):
    global index
    global angle
    r = requests.post('http://192.168.0.25', data = {'angle':angle_form})
    angle = r.text[6:]
    now_time = datetime.now()
    cnx = sql.connect("localhost", "root", "ksemwetipg", "mydb")
    cursor = cnx.cursor()
    query = ("insert into servo  VALUES (%s, %s, %s)")
    cursor.execute(query, (index, angle, now_time))
    cnx.commit()
    cursor.close()
    cnx.close()
    url = "http://alfa.smartstorm.io/api/v1/measure"
    data = {"user_id": "etipany@eti.pl",
            "sensor_id": "5a5ddf932a455b457fba826f",
            "desc": "angle",
            "measure_value": angle}
    r = requests.post(url, data)
    index = index + 1
    return 0

@app.route('/form/', methods = ["POST"])
def form():
    angle_form = request.form['angle']
    send_Data(angle_form)
    response = jsonify()
    response.status_code = 205
    return response

@app.route('/postAngle/', methods = ["POST"])
def postAngles():
    global angle
    cnx = sql.connect("localhost", "root", "ksemwetipg", "mydb")
    cursor = cnx.cursor()
    query = "select * from servo"
    cursor.execute(query)
    result = cursor.fetchall()

    i = 0
    data = []
    date = []
    avg = []
    x = []
    trend = []
    # Getting last index from database
    if (not (len(result) == 0)):
        for r in result:
            data.append(r[1])
            date.append(r[2])

        average = sum(data) / len(data)
        for i in range(0, len(data)):
            avg.append(average)
            x.append(i)

        if(len(data)>=2):
            z = numpy.polyfit(x, data, 1)
            p = numpy.poly1d(z)
            tr = p(x)
            for t in tr:
                trend.append(t)

    cnx.commit()

    cursor.close()
    cnx.close()

    return jsonify(angle=angle,
                   data=data,
                   date=date,
                   avg=avg,
                   trend=trend)

@app.route('/postDataset/', methods = ["POST"])
def postDataset():
    cnx = sql.connect("localhost", "root", "ksemwetipg", "mydb")
    cursor = cnx.cursor()
    query = "select * from servo"
    cursor.execute(query)
    result = cursor.fetchall()

    i = 0
    data = []
    date = []
    avg = []
    x = []
    trend = []
    # Getting last index from database
    if (not (len(result) == 0)):
        for r in result:
            data.append(r[1])
            date.append(r[2])

    average = sum(data)/len(data)
    for i in range(0, len(data)):
        avg.append(average)
        x.append(i)


    z = numpy.polyfit(x, data, 1)
    p = numpy.poly1d(z)
    tr = p(x)
    for t in tr:
        trend.append(t)

    cnx.commit()

    cursor.close()
    cnx.close()
    return jsonify(data = data,
                   date = date,
                   avg = avg,
                   trend = trend)


if __name__ == '__main__':
    app.run(host=ip_adress)
