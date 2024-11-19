# app_controller.py
from flask import Flask, render_template, current_app, session, redirect, url_for, request, jsonify
from models.db import db, instance
from controllers.sensors_controller import sensor_
from controllers.actuators_controller import actuator_
from controllers.reads_controller import read
from controllers.writes_controller import write
from controllers.users_controller import user, login_required
from models.iot.devices import *
from models.iot.sensors import *
from models.iot.actuators import *
from models.iot.read import *
from models.iot.write import *
import paho.mqtt.client as mqtt
import time


def create_app():
    app = Flask(__name__, template_folder="./views/", static_folder="./static/", root_path="./")
    
    app.register_blueprint(sensor_, url_prefix='/')
    app.register_blueprint(actuator_, url_prefix='/')
    app.register_blueprint(read, url_prefix='/')
    app.register_blueprint(write, url_prefix='/')
    app.register_blueprint(user, url_prefix='/')

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    app.config['MQTT_BROKER_URL'] = 'mqtt-dashboard.com'
    app.config['MQTT_BROKER_PORT'] = 1883

    with app.app_context():
        mqtt_handler = MQTTHandler(app)
        app.mqtt_handler = mqtt_handler
    
    @app.route('/')
    @login_required
    def index():
        with app.app_context():
            sensors_data = []
            active_sensors = Sensor.query.join(Device).filter(Device.is_active == True).all()
            for sensor in active_sensors:
                last_read = Read.query.filter(Read.sensors_id == sensor.id).order_by(Read.read_datetime.desc()).first()
                sensors_data.append({
                    'name': sensor.topic.replace('trabFinal_', ''),
                    'value': last_read.value if last_read else 'Sem leitura',
                    'unit': sensor.unit
                })
            return render_template("home.html", sensors=sensors_data)

    @app.route('/logoff')
    def logoff():
        # Limpa todos os dados da sessão
        session.clear()
        # Redireciona para a página de login
        return render_template("login.html")

    @app.route('/home')
    @login_required
    def home():
        with app.app_context():
            sensors_data = []
            active_sensors = Sensor.query.join(Device).filter(Device.is_active == True).all()
            for sensor in active_sensors:
                last_read = Read.query.filter(Read.sensors_id == sensor.id).order_by(Read.read_datetime.desc()).first()
                sensors_data.append({
                    'name': sensor.topic.replace('trabFinal_', ''),
                    'value': last_read.value if last_read else 'Sem leitura',
                    'unit': sensor.unit
                })
            return render_template("home.html", sensors=sensors_data)
        
    @app.route('/publish')
    @login_required
    def publish():
        with current_app.app_context():
            # Busca atuadores ativos
            actuators = Actuator.query.join(Device).filter(Device.is_active == True).all()
        return render_template("publish.html", actuators=actuators)

    
    @app.route('/publish_message', methods=['POST'])
    @login_required
    def publish_message():

        data = request.get_json()
        actuator_id = data.get('actuator_id')  # Recebe o ID do atuador.
        message = data.get('message')

        if not actuator_id or message is None:
            return jsonify({'status': 'error', 'message': 'ID do atuador ou mensagem não fornecidos'}), 400

        try:
            # Busca o atuador no banco de dados.
            actuator = Actuator.query.filter_by(id=actuator_id).join(Device).filter(Device.is_active == True).first()

            if not actuator:
                return jsonify({'status': 'error', 'message': 'Atuador não encontrado ou inativo'}), 404

            topic = actuator.topic  # Obtém o tópico associado ao atuador.

            with current_app.app_context():
                mqtt_handler = current_app.mqtt_handler
                mqtt_handler.publish(topic, message)

            return jsonify({'status': 'success', 'message': f'Mensagem publicada no tópico {topic}'}), 200
        except Exception as e:
            print(f"Erro ao publicar mensagem: {e}")
            return jsonify({'status': 'error', 'message': str(e)}), 500

    return app


class MQTTHandler:
    def __init__(self, app):
        self.app = app
        self.client = None
        self.connect()

    def connect(self):
        try:
            if self.client is None:
                self.client = mqtt.Client()
                self.client.on_connect = self.on_connect
                self.client.on_message = self.on_message

                self.client.reconnect_delay_set(min_delay=1, max_delay=120)

            # Evita múltiplas tentativas simultâneas
            if not self.client.is_connected():
                with self.app.app_context():
                    broker_url = self.app.config['MQTT_BROKER_URL']
                    broker_port = self.app.config['MQTT_BROKER_PORT']

                print("Tentando conectar ao broker MQTT...")
                self.client.connect(broker_url, broker_port, keepalive=120)

            # Start the loop once
            if not self.client._thread:
                print("Iniciando loop MQTT...")
                self.client.loop_start()


        except Exception as e:
            print(f"MQTT Connection Error: {e}")
            time.sleep(5)
            self.connect()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print('MQTT Broker Connected successfully')
            with self.app.app_context():
                active_sensor_topics = Sensor.query.join(Device).filter(Device.is_active == True).with_entities(Sensor.topic).all()
                active_actuator_topics = Actuator.query.join(Device).filter(Device.is_active == True).with_entities(Actuator.topic).all()
                for topic in active_sensor_topics + active_actuator_topics:
                    client.subscribe(topic[0])
                    print(f"Subscribed to topic: {topic[0]}")
        else:
            print(f'Bad connection. Code: {rc}')
            self.connect()

    def on_message(self, client, userdata, message):
        with self.app.app_context():
            try:
                topic = message.topic
                payload = message.payload.decode()
                value = float(payload)

                sensor = Sensor.query.filter(Sensor.topic == topic).first()
                if sensor:
                    Read.save_read(topic, value)
                    print(f"Novos dados do topico {topic} salvo")

                actuator = Actuator.query.filter(Actuator.topic == topic).first()
                if actuator:
                    Write.save_write(topic, value)
                    print(f"Novos dados do topico {topic} salvo")

            except Exception as e:
                print(f"Message processing error: {e}")
                print(message.payload.decode())
    
    def publish(self, topic, message):
        try:
            if self.client and self.client.is_connected():
                self.client.publish(topic, message)
                print(f"Mensagem publicada: {message} no tópico: {topic}")
            else:
                print("Cliente MQTT desconectado, tentando reconectar...")
                self.connect()
                self.client.publish(topic, message)
        except Exception as e:
            print(f"Erro ao publicar no tópico {topic}: {e}")
