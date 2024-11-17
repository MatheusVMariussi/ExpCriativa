#app_controller.py
from flask import Flask, render_template, request
from models.db import db, instance

def create_app():
    app = Flask(__name__,
                template_folder="./views/",
                static_folder="./static/",
                root_path="./")
    

    app.config['TESTING'] = False
    app.config['SECRET_KEY'] = 'generated-secrete-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = instance
    db.init_app(app)

    @app.route('/')
    def index():
        return render_template("home.html")
    
    return app
