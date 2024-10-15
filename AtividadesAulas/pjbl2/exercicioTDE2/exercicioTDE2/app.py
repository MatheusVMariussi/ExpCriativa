from flask import Flask, render_template, request, redirect, url_for, jsonify, session, abort
from devices import devices_bp
from errorHandler import error
from login import login_bp, login_required, admin_required  # Importando os decoradores
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
import json

# https://wokwi.com/projects/410554286481975297

temperature = 10
humidity = 10

app = Flask(__name__)

# Configuração da chave secreta para as sessões
app.secret_key = 'chaveExtremamenteSecreta'

# Registro de blueprints
app.register_blueprint(error, url_prefix='/')
app.register_blueprint(login_bp, url_prefix='/')
app.register_blueprint(devices_bp, url_prefix='/')

app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_USERNAME'] = ''
app.config['MQTT_PASSWORD'] = ''
app.config['MQTT_KEEPALIVE'] = 5000
app.config['MQTT_TLS_ENABLED'] = False

mqtt_client = Mqtt()
mqtt_client.init_app(app)

topic_subscribe1 = "aula0110exp/temperatura"
topic_subscribe2 = "aula0110exp/umidade"
topic_publish = "aula0110exp/publish"

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/logoff')
def logoff():
    session.pop('user', None)  # Remove o usuário da sessão
    return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    return render_template("home.html")

@app.route('/tempo_real')
@login_required
def tempo_real():
    global temperature, humidity
    values = {"temperature": temperature, "humidity": humidity}
    return render_template("tr.html", values=values)

@login_required
@app.route('/publish')
def publish():
    return render_template('publish.html')

@app.route('/publish_message', methods=['GET','POST'])
def publish_message():
    request_data = request.get_json()
    publish_result = mqtt_client.publish(request_data['topic'], request_data['message'])
    return jsonify(publish_result)

@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Broker Connected successfully')
        mqtt_client.subscribe(topic_subscribe1)  # subscribe topic
        mqtt_client.subscribe(topic_subscribe2)  # subscribe topic
    else:
        print('Bad connection. Code:', rc)

@mqtt_client.on_disconnect()
def handle_disconnect(client, userdata, rc):
    print("Disconnected from broker")

@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    # Processar as mensagens MQTT recebidas
    decoded_message = message.payload.decode()

    # Atualizando outras variáveis globais se necessário
    if message.topic == topic_subscribe1:
        global temperature
        temperature = decoded_message
    if message.topic == topic_subscribe2:
        global humidity
        humidity = decoded_message

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
