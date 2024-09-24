from flask import Flask, render_template, request

app = Flask(__name__)

# Initialize global dictionaries for users, sensors, and actuators
users = {}
sensors = {}
actuators = {}

@app.route('/')
def login():
    return render_template("login.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/register_user')
def register_user():
    return render_template("register_user.html", users=users)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
    else:
        user = request.args.get('user', None)
        password = request.args.get('password', None)
    
    if user and password:
        users[user] = password
    return render_template("users.html", users=users)

@app.route('/remove_user')
def remove_user():
    return render_template("remove_user.html", users=users)
                           
@app.route('/del_user', methods=['GET','POST'])
def del_user():
    if request.method == 'POST':
        user = request.form['user']
    else:
        user = request.args.get('user', None)
    users.pop(user)
    return render_template("users.html", users=users)

@app.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        user = request.form['user']
        password = request.form['password']
        if user in users and users[user] == password:
            return render_template('home.html')
        else:
            return """<h1>Invalid credentials!</h1> 
                    <p>Voltar para <a href="/">página de login</a>!</p>
                    """
    return render_template('login.html')

@app.route('/users')
def list_users():
    return render_template("users.html", users=users)

@app.route('/sensors')
def sensors_view():
    return render_template("sensors.html", sensors=sensors)

@app.route('/register_sensor')
def reg_sensor():
    return render_template("register_sensor.html")

@app.route('/add_sensor', methods=['GET', 'POST'])
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

@app.route('/remove_sensor')
def remove_sensor():
    return render_template("remove_sensor.html", sensors=sensors)
                           
@app.route('/del_sensor', methods=['GET','POST'])
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

@app.route('/actuators')
def actuators_view():
    return render_template("actuators.html", actuators=actuators)

@app.route('/register_actuator')
def reg_actuator():
    return render_template("register_actuator.html")

@app.route('/add_actuators', methods=['GET', 'POST'])
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

@app.route('/remove_actuator')
def remove_actuator():
    return render_template("remove_actuator.html", actuators=actuators)
                           
@app.route('/del_actuators', methods=['GET','POST'])
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
