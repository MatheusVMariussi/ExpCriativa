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
def login():
    return render_template("login.html")

@app.route('/home')
def index():
    return render_template("home.html")

@app.route('/quarto')
def quarto():
    itensDaCasa = {'Sensor de Luminosidade':'/quarto', 'Interruptor':'/quarto'}
    return render_template("quarto.html", itensDaCasa=itensDaCasa)

@app.route('/banheiro')
def banheiro():
    itensDaCasa = {'Sensor de Umidade':'/banheiro', 'Lâmpada Inteligente':'/banheiro'}
    return render_template("banheiro.html", itensDaCasa=itensDaCasa)

@app.route('/sala')
def sala():
    return render_template("sala.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
