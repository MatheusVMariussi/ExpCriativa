from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sensores')
def sensors():
    sensores = {'T1':56, 'T2':25, 'T3':15}
    return render_template("sensores.html", sensores=sensores)

@app.route('/actuators')
def actuators():
    actuators = {'Servo Motor':1, 'Lâmpada':0}
    return render_template("actuators.html", actuators=actuators)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)