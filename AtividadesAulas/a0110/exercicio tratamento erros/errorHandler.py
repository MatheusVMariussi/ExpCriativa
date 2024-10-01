# errorHandler.py
from flask import Blueprint, request, render_template, redirect, url_for

error = Blueprint("error",__name__, template_folder="templates")

@error.errorhandler(200)
def page_not_found(error):
    return render_template('200.html'), 200

@error.errorhandler(401)
def page_not_found(error):
    return render_template('401.html'), 401

@error.errorhandler(403)
def page_not_found(error):
    return render_template('403.html'), 403

@error.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@error.errorhandler(405)
def page_not_found(error):
    return render_template('405.html'), 405

@error.errorhandler(408)
def page_not_found(error):
    return render_template('408.html'), 408

@error.errorhandler(429)
def page_not_found(error):
    return render_template('429.html'), 429

@error.errorhandler(500)
def page_not_found(error):
    return render_template('500.html'), 500

@error.errorhandler(503)
def page_not_found(error):
    return render_template('503.html'), 503