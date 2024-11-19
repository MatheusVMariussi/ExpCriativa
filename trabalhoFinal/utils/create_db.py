#create_db.py
from flask import Flask
from models import *

def create_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
        Role.save_role("Admin", "Usuário full")
        Role.save_role("User", "Usuário com limitações")
        
        User.save_user("Admin","Admin", "admin","admin")
        User.save_user("User","Teste", "Teste","teste")

        Sensor.save_sensor("Temperatura", "DHT", "22", "trabFinal_Temperatura", "ºC", True)
        Sensor.save_sensor("Umidade", "DHT", "22", "trabFinal_Umidade", "%", True)
        Sensor.save_sensor("Amonia", "MQ-135", "135", "trabFinal_Amonia", "%", True)
        Sensor.save_sensor("CO2", "MQ-135", "135", "trabFinal_Co2", "%", True)

        Actuator.save_actuator("Lampada", "LED", "Led", "trabFinal_Lampada", " ", True)
        Actuator.save_actuator("Chave Master", "Slide switch", "slider", "trabFinal_Slider", " ", True)