import os



from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect




db = SQLAlchemy()

def create_app():

    app = Flask(__name__)

    app.config.from_object('config.ProductionConfig')
    csrf = CSRFProtect(app)

    db.init_app(app)

    from . import home
    from . import auth
    from . import user
    from . import models

    app.register_blueprint(home.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(user.bp)

    with app.app_context():
        db.create_all()


    @app.after_request
    def prepare_response(response):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        #response.headers['Content-Security-Policy'] = "default-src 'self'; style-src 'self' https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css;"
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        return response

    return app


my_app = create_app()
