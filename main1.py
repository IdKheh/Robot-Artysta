from flask import Flask, render_template,request
import serial
import time

ser = serial.Serial('/dev/ttyACM0',9600, timeout =1)
state = 0
app= Flask(__name__)
@app.route('/')
def index():
    now = '30.10.2023'
    
    templateData = { 'time': now }
    action()
    return render_template('index_a.html', **templateData)

@app.route('/', methods=['GET','POST'])
def action():
    print(request.method)
    if request.method=='POST' or request.method=='GET':
        if request.form.get('dioda1')=='dioda1':
            print("dioda1")
            state = 1
            ser.write(str(state).encode('utf-8'))
        elif request.form.get('dioda2') == 'dioda2':
            print("dioda2")
            state=2
            ser.write(str(state).encode('utf-8'))
        elif request.form.get('dioda3')=='dioda3':
            print("dioda3")
            state=3
            ser.write(str(state).encode('utf-8'))
        elif request.form.get('dioda4')=='dioda4':
            print("dioda4")
            state=4
            ser.write(str(state).encode('utf-8'))
        elif request.form.get('obrazek')=='obrazek':
            print("obrazek")
            state=0
            ser.write(str(state).encode('utf-8'))
        else:
            print(":(")
    else:
        ser.write(str(0).encode('utf-8'))
    return render_template('index_a.html')
    
    
    
    
if __name__ == '__main__':
    app.run(debug = True, port = 80, host = '0.0.0.0')
    ser.reset_input_buffer()