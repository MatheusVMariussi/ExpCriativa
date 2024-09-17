from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/sensores')
def sensors():
    sensores = ['Umidade', 'Temperatura', 'Luminosidade']
    return render_template("sensores.html", sensores=sensores)

@app.route('/actuators')
def actuators():
    actuators = ['Servo Motor', 'Lâmpada']
    return render_template("actuators.html", actuators=actuators)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)