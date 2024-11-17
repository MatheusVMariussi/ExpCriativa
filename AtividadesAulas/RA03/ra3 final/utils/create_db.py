#create_db.py
from flask import Flask
from models import *

def create_db(app:Flask):
    with app.app_context():
        db.drop_all()
        db.create_all()
        Role.save_role("Admin", "Usuário full")
        Role.save_role("User", "Usuário com limitações")
        
        User.save_user("Admin","Admin", "admin","admin")