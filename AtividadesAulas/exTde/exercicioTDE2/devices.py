#devices.py
from flask import Blueprint, request, render_template

devices_bp = Blueprint("devices",__name__, template_folder="templates")

actuators = {}
sensors = {"DHT22":"10:10"}

@devices_bp.route('/devices')
def devices():
    global sensors, actuators
    return render_template('devices.html', sensors=sensors, actuators=actuators)

@devices_bp.route('/add_sensor', methods=['GET', 'POST'])
def add_sensor():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
    else:
        key = request.args.get('key', None)
        value = request.args.get('value', None)
    
    if key and value:
        sensors[key] = value
    return render_template('devices.html', sensors=sensors, actuators=actuators)

@devices_bp.route('/del_sensor', methods=['GET','POST'])
def del_sensor():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
    else:
        key = request.args.get('key', None)
        value = request.args.get('value', None)

    if key and value:
        sensors.pop(key)
    
    return render_template('devices.html', sensors=sensors, actuators=actuators)

@devices_bp.route('/add_actuators', methods=['GET', 'POST'])
def add_actuators():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
    else:
        key = request.args.get('key', None)
        value = request.args.get('value', None)
    
    if key and value:
        actuators[key] = value
    return render_template('devices.html', sensors=sensors, actuators=actuators)

@devices_bp.route('/del_actuators', methods=['GET','POST'])
def del_actuator():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
    else:
        key = request.args.get('key', None)
        value = request.args.get('value', None)

    if key and value:
        actuators.pop(key)
    
    return render_template('devices.html', sensors=sensors, actuators=actuators)