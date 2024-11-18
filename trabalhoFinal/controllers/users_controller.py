#users_controller.py
from flask import Blueprint, request, render_template, redirect, url_for, session, abort
from functools import wraps
from models.user.users import User
from models.user.roles import Role

user = Blueprint("user",__name__, template_folder="views")

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

@user.route('/register_user')
def register_user():
    roles = Role.get_role()
    return render_template("register_user.html", roles=roles)

@user.route('/add_user', methods=['POST'])
@admin_required
def add_user():
    global users
    if request.method == 'POST':
        role_name = request.form['role_type_']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        User.save_user(role_name, username, email,password)
        users = User.get_users()
        return render_template("users.html", devices=users)

@user.route('/edit_user')
@admin_required
def edit_user():
    email = request.args.get('email', None)
    # Verifica se é admin antes de permitir edição
    if email and User.is_admin(email):
        return redirect(url_for('user.users'))
    
    users = User.query.filter(User.email == email)\
        .join(Role).add_columns(User.id, User.username, 
                               User.email, Role.name.label('role')).all()
    roles = Role.get_role()
    return render_template("update_user.html", users=users, roles=roles)

@user.route('/update_user', methods=['POST'])
@admin_required
def update_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role_type_ = request.form['role_type_']
        
        if User.is_admin(email):
            return redirect(url_for('user.users'))
        
        users = User.update_user(username, email, password, role_type_)
        return render_template("users.html", devices=users)

@user.route('/del_user')
def del_user():
    email = request.args.get('email', None)
    if email:
        if User.is_admin(email):
            return redirect(url_for('user.users'))
        users = User.delete_user(email)
        return render_template("users.html", devices=users)
    return redirect(url_for('user.users'))

@user.route('/users')
def users():
    users = User.get_users()
    return render_template("users.html", devices=users)

@user.route('/validated_user', methods=['POST'])
def validated_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Busca o usuário e seu role no banco de dados
        user_data = User.query.filter(User.email == email)\
            .join(Role).add_columns(User.password, Role.name.label('role')).first()
        
        # Verifica se o usuário existe e a senha está correta
        if user_data and user_data[1] == password:  # user_data[1] contém a senha
            # Busca os dados completos do usuário
            user_info = User.query.filter_by(email=email).first()
            
            # Armazena informações do usuário na sessão
            session['user'] = user_info.username
            session['email'] = user_info.email
            session['role'] = user_data.role
            
            # Se for admin, marca na sessão
            if user_data.role == 'Admin':
                session['user'] = 'admin'
            
            return redirect(url_for('index'))
        else:
            # Em caso de credenciais inválidas, redireciona para login com mensagem de erro
            return render_template('login.html', error="Credenciais inválidas")
    
    # Se não for POST, redireciona para página de login
    return redirect(url_for('index'))