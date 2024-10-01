#sensors.py
from flask import Blueprint, request, render_template, redirect, url_for

sensors_bp = Blueprint("sensors",__name__, template_folder="templates")

sensors = {"DHT22":"10:10"}

@sensors_bp.route('/sensors')
def sensors_view():
    return render_template("sensors.html", sensors=sensors)

@sensors_bp.route('/register_sensor')
def reg_sensor():
    return render_template("register_sensor.html")

@sensors_bp.route('/add_sensor', methods=['GET', 'POST'])
def add_sensor():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
    else:
        key = request.args.get('key', None)
        value = request.args.get('value', None)
    
    if key and value:
        sensors[key] = value
    return render_template("sensors.html", sensors=sensors)

@sensors_bp.route('/remove_sensor')
def remove_sensor():
    return render_template("remove_sensor.html", sensors=sensors)
                           
@sensors_bp.route('/del_sensor', methods=['GET','POST'])
def del_sensor():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
    else:
        key = request.args.get('key', None)
        value = request.args.get('value', None)

    if key and value:
        sensors.pop(key)
    
    return render_template("sensors.html", sensors=sensors)