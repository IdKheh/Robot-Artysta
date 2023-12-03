from flask import Flask, render_template, redirect, url_for, flash
import serial
import os
import sqlite3
from PIL import Image
from PIL import ImageDraw

# ser = serial.Serial('/dev/ttyACM0',9600, timeout =1) //polaczenie ardiuno i raspberry
serGPS = serial.Serial('/dev/ttyUSB0',9600) # polaczenie raspberry i GPS
conn = sqlite3.connect('GPSData.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS DATA(id INTEGER PRIMARY KEY, x INTEGER, y INTEGER);''')
app = Flask(__name__)
app.secret_key = "secret key"

## dodaj statyczny adres IP: https://www.instructables.com/Raspberry-Pi-GPS-Tracker/
## jakiś tutorial https://www.youtube.com/watch?v=4R5m7xsU-0g

@app.route('/')
def index():
    action(0)
    return render_template('index.html')


@app.route('/<FUNCTION>')
def execCommand(FUNCTION = None):
    exec(FUNCTION.replace("<br>", "\n"))
    return ""


def draw_and_return(coordinates):
    img = Image.new("RGB", (1000, 1000), color = (255, 255, 255))
    img1 = ImageDraw.Draw(img)
    positionX = coordinates[0][0]
    positionY = coordinates[0][1]
    for i in range(1,len(coordinates)-1):

        start = (positionX - coordinates[i][0], positionY - coordinates[i][1])
        end = (positionX - coordinates[i+1][0], positionY - coordinates[i+1][1])
        img1.line((start, end),fill=0, width=2)

    img.save(f"static/img.png")


def action(direction : int):
    # ser.write(str(direction).encode('utf-8'))

    makeData()
    return ''


def delete():
    cursor.execute("DROP TABLE DATA;")


def insert(x: float, y: float):
    cursor.execute("INSERT INTO DATA (x, y) VALUES(?,?)", (x, y))


def select(l: list):
    cursor.execute("SELECT * FROM DATA;")
    records = cursor.fetchall()
    for row in records:
        t = []
        t.append(row[1])
        t.append(row[2])
        l.append(t)
    conn.commit()


def makeData():
    while(True):
        nmea_sentence = serGPS.readline()
        message = nmea_sentence.decode("utf-8").replace("\n", "").replace("\r", "").split(',')
        if message[0] == '$GPGGA':
            if (message[2] != '' and message[4] != ''):
                x = int(message[2].replace(".", ""))
                y = int(message[4].replace(".", ""))
                insert(x, y)
                break


def deleteFile():
    os.remove("static/img.png")


def draw():
    action(8)  # blokada ruchu robota
    l = []
    select(l)
    draw_and_return(l)
    action(9)
    return ''

def reset():
    delete()
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS DATA(id INTEGER PRIMARY KEY, x INTEGER, y INTEGER);''')
    conn.commit()
    deleteFile()
    return ''


def poweroff():
    delete()
    conn.commit()
    cursor.close()
    deleteFile()
    # os.system('shutdown')
    return ''


if __name__ == '__main__':
    app.run()
    # app.run(debug=True, port=80, host='0.0.0.0')
    # ser.reset_input_buffer()