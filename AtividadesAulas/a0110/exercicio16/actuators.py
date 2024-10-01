#actuators.py
from flask import Blueprint, request, render_template, redirect, url_for

actuators_bp = Blueprint("actuators",__name__, template_folder="templates")

actuators = {}

@actuators_bp.route('/actuators')
def actuators_view():
    return render_template("actuators.html", actuators=actuators)

@actuators_bp.route('/register_actuator')
def reg_actuator():
    return render_template("register_actuator.html")

@actuators_bp.route('/add_actuators', methods=['GET', 'POST'])
def add_actuators():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
    else:
        key = request.args.get('key', None)
        value = request.args.get('value', None)
    
    if key and value:
        actuators[key] = value
    return render_template("actuators.html", actuators=actuators)

@actuators_bp.route('/remove_actuator')
def remove_actuator():
    return render_template("remove_actuator.html", actuators=actuators)
                           
@actuators_bp.route('/del_actuators', methods=['GET','POST'])
def del_actuator():
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
    else:
        key = request.args.get('key', None)
        value = request.args.get('value', None)

    if key and value:
        actuators.pop(key)
    
    return render_template("actuators.html", actuators=actuators)