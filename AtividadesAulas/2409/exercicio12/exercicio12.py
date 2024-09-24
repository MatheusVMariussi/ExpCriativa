from flask import Flask, render_template, request

app = Flask(__name__)

users = {
    'user1': '1234',
    'user2': '1234'
}

@app.route('/login', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        print(user, password)
        if user in users and users[user] == password:
            return render_template('home.html')
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template("home.html")

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