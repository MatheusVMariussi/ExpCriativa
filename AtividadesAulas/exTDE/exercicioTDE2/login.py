# login.py
from flask import Blueprint, request, render_template, redirect, url_for

login_bp = Blueprint("login",__name__, template_folder="templates")

users = { "user1":"1234" }

@login_bp.route("/users", methods=["GET", "POST"])
def manage_users():
    global users
    if request.method == "POST":
        if 'user' in request.form and 'password' in request.form:
            user = request.form["user"]
            password = request.form["password"]

            # Se for para cadastrar um usuário
            if request.form.get('action') == 'register':
                users[user] = password
            # Se for para remover um usuário
            elif request.form.get('action') == 'remove':
                if user in users and users[user] == password:
                    del users[user]

        return redirect(url_for('manage_users'))

    return render_template("users.html", users=users)

@login_bp.route('/add_user', methods=['GET', 'POST'])
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

@login_bp.route('/del_user', methods=['GET','POST'])
def del_user():
    if request.method == 'POST':
        user = request.form['user']
    else:
        user = request.args.get('user', None)
    users.pop(user)
    return render_template("users.html", users=users)

@login_bp.route('/validated_user', methods=['POST'])
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