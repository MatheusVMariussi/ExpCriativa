from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/quarto')
def quarto():
    itensDaCasa = {'Sensor de Luminosidade':'/quarto', 'Interruptor':'/quarto'}
    return render_template("quarto.html", itensDaCasa=itensDaCasa)

@app.route('/banheiro')
def banheiro():
    itensDaCasa = {'Sensor de Umidade':'/banheiro', 'Lâmpada Inteligente':'/banheiro'}
    return render_template("banheiro.html", itensDaCasa=itensDaCasa)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)