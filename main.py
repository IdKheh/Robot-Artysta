from flask import Flask, render_template, redirect, url_for, flash, send_from_directory
import serial
import os
import sqlite3
from PIL import Image
from PIL import ImageDraw
from werkzeug.utils import secure_filename

ser = serial.Serial('/dev/ttyACM0',9600, timeout =1) #polaczenie ardiuno i raspberry
serGPS = serial.Serial('/dev/ttyUSB0',9600) # polaczenie raspberry i GPS
conn = sqlite3.connect('GPSData.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS DATA(id INTEGER PRIMARY KEY, x INTEGER, y INTEGER);''')
app = Flask(__name__)
app.secret_key = "secret key"

@app.route('/')
def index():
    ser.write(str(0).encode('utf-8'))
    ser.write(str(9).encode('utf-8'))
    
    return render_template('index.html')


@app.route('/<FUNCTION>')
def execCommand(FUNCTION = None):
    exec(FUNCTION.replace("<br>", "\n"))
    return ""


def draw_and_return(coordinates,number):
    print(coordinates)
    img = Image.new("RGB", (500, 500), color = (255, 255, 255))
    img1 = ImageDraw.Draw(img)
    
    try:
        positionX = coordinates[0][0]
        positionY = coordinates[0][1]
                
        for i in range(1,len(coordinates)-1):

            start = (abs(coordinates[i][0]-positionX)/50, abs(coordinates[i][1]-positionY)/50)
            end = (abs(coordinates[i+1][0]-positionX)/50, abs(coordinates[i+1][1]-positionY)/50)
            print(start)
            print(end)
            img1.line((start, end),fill=5, width=5)
    except:
        print('ERROR: IMG')
        start = (0,0)
        img1.line((start, start),fill=5, width=2)

    print(number)
    img.save(f"static/img"+str(number)+".png")


def action(direction : int):
    ser.write(str(direction).encode('utf-8'))
    makeData()
    return ''


def delete():
    cursor.execute("DROP TABLE DATA;")


def insert(x: float, y: float):
    cursor.execute("INSERT INTO DATA (x, y) VALUES(?,?)", (x, y))
    conn.commit()


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
    errors = 0
    while(errors<20):
        try:
            nmea_sentence = serGPS.readline()
            message = nmea_sentence.decode("utf-8").replace("\n", "").replace("\r", "").split(',')
            if message[0] == '$GPGGA':
                if (message[2] != '' and message[4] != ''):
                    x = int(message[2].replace(".", ""))
                    y = int(message[4].replace(".", ""))
                    print(x,y)
                    insert(x,y)
                    errors = 100
                    break
        except:
            errors +=1
            print('ERROR: GPS')
            pass

def deleteFile(number):
    for i in range(1,number+1):
        os.remove('static/img'+str(i)+'.png')


def draw(number : int):
    print("number: "+str(number))
    counter= number
    action(8)  # blokada ruchu robota
    l = []
    select(l)
    draw_and_return(l,number)
    action(9)
    return ""
    

def reset(number : int):
    delete()
    conn.commit()
    cursor.execute('''CREATE TABLE IF NOT EXISTS DATA(id INTEGER PRIMARY KEY, x INTEGER, y INTEGER);''')
    conn.commit()
    #deleteFile(number)
    return ''


def poweroff(number : int):
    delete()
    conn.commit()
    cursor.close()
    deleteFile(number)
    os.system('shutdown -h now')
    return ''


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
    ser.reset_input_buffer()
