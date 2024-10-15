from flask import Blueprint, request, render_template, redirect, url_for, session, abort
from functools import wraps

login_bp = Blueprint("login", __name__, template_folder="templates")

users = {"admin": "admin", "tester" : "tester"}

# Decorador para exigir login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Decorador para exigir que o usuário seja admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user') != 'admin':
            abort(403)  # Retorna "403 Forbidden" se o usuário não for admin
        return f(*args, **kwargs)
    return decorated_function

@login_bp.route("/users", methods=["GET", "POST"])
@admin_required
def manage_users():
    global users
    if request.method == "POST":
        if 'user' in request.form and 'password' in request.form:
            user = request.form["user"]
            password = request.form["password"]
            if request.form.get('action') == 'register':
                users[user] = password
            elif request.form.get('action') == 'remove':
                if user in users and users[user] == password:
                    del users[user]
        return redirect(url_for('manage_users'))
    return render_template("users.html", users=users)

@login_bp.route('/add_user', methods=['GET', 'POST'])
@admin_required
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

@login_bp.route('/del_user', methods=['GET', 'POST'])
@admin_required
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
            session['user'] = user  # Salva o usuário na sessão
            return render_template('home.html')
        else:
            return render_template('erroLogin.html')
    return render_template('login.html')
