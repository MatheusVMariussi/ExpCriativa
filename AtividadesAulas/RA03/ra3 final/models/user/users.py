#users.py
from models.db import db
from models.user.roles import Role

class User(db.Model):
    __tablename__= "users"
    id = db.Column("id", db.Integer(), primary_key=True)
    role_id = db.Column( db.Integer, db.ForeignKey(Role.id))
    username= db.Column(db.String(45) , nullable=False, unique=True)
    email= db.Column(db.String(30), nullable=False, unique=True)
    password= db.Column(db.String(256) , nullable=False)

    def save_user(role_type_, username, email, password):
        role = Role.get_single_role(role_type_)
        user = User(role_id = role.id, username = username, email = email, password = (password))
        db.session.add(user)
        db.session.commit()

    def get_users():
        users = User.query.join(Role, Role.id == User.role_id)\
            .add_columns(User.id, User.username, User.email, Role.name.label('role')).all()
        return users

    def get_single_user(id):
        user = User.query.filter(User.id == id).join(Role).add_columns(
            User.id, User.username, User.email, Role.name.label('role')).first()
        return user

    def is_admin(email):
        user = User.query.filter(User.email == email)\
            .join(Role).add_columns(Role.name.label('role')).first()
        return user is not None and user.role == 'Admin'

    def update_user(username, email, password, role_type_):
        user = User.query.filter(User.email == email).first()
        # Verifica se é admin antes de permitir alteração
        if user is not None and not User.is_admin(email):
            role = Role.get_single_role(role_type_)
            user.username = username
            user.password = password
            user.role_id = role.id
            db.session.commit()
        return User.get_users()

    def delete_user(email):
        # Verifica se é admin antes de deletar
        if not User.is_admin(email):
            user = User.query.filter(User.email == email).first()
            if user is not None:
                db.session.delete(user)
                db.session.commit()
        return User.get_users()