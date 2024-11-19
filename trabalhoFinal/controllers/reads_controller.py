#reads_controller.py
from flask import Blueprint, request, render_template
from models.iot.read import Read
from models.iot.sensors import Sensor
from controllers.users_controller import login_required

read = Blueprint("read",__name__, template_folder="views")

@read.route("/history_read")
@login_required
def history_read():
    sensors = Sensor.get_sensors()
    read = {}
    return render_template("history_read.html", sensors = sensors, read = read)

@read.route("/get_read", methods=['POST'])
def get_read():
    if request.method == 'POST':
        id = request.form['id']
        start = request.form['start']
        end = request.form['end']
        read = Read.get_read(id, start, end)
        
        sensors = Sensor.get_sensors()
        return render_template("history_read.html", sensors = sensors, read = read)