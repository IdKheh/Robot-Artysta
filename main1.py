from flask import Flask, render_template, request
# import serial

# ser = serial.Serial('/dev/ttyACM0',9600, timeout =1)
app = Flask(__name__)


@app.route('/')
def index():
    action(0)
    return render_template('index_a.html')


@app.route('/<FUNCTION>')
def execCommand(FUNCTION = None):
    exec(FUNCTION.replace("<br>","\n"))
    return ""


def action(kierunek:int):
    #ser.write(str(kierunek).encode('utf-8'))
    print(kierunek)
    return render_template('index_a.html')

def draw():
    print(':)')
    return render_template('index_a.html')

if __name__ == '__main__':
    app.run()
    #app.run(debug=True, port=80, host='0.0.0.0')
    # ser.reset_input_buffer()



