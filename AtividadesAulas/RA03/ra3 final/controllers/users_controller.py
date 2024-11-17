#users_controller.py
from flask import Blueprint, request, render_template, redirect, url_for
from models.user.users import User
from models.user.roles import Role

user = Blueprint("user",__name__, template_folder="views")

@user.route('/register_user')
def register_user():
    roles = Role.get_role()
    return render_template("register_user.html", roles=roles)

@user.route('/add_user', methods=['POST'])
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