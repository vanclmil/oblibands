from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)
app.secret_key = b'necumtohlejesecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://vjetname_admin:admin123@vjetname.heliohost.org/vjetname_oblibands"


db.init_app(app)
login_manager.init_app(app)

with app.app_context():
    from models import *
    # Create Database Models
    db.create_all()

    import routes
    import auth

    # Register Blueprints
    app.register_blueprint(routes.main_bp)
    app.register_blueprint(auth.auth_bp)


if __name__ == '__main__':
    app.run()
