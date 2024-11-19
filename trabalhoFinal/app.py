# app.py
from controllers.app_controller import create_app
from utils.create_db import create_db

if __name__ == "__main__":
    app = create_app()
    create_db(app)
    app.run(host='0.0.0.0', use_reloader=False, port=8080, debug=True)


# https://wokwi.com/projects/414944648253741057