from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask import Flask
from flask_login import LoginManager

from user.middleware import Middleware

db = SQLAlchemy()
UPLOAD_FOLDER = './static/upload'
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

login_manager = LoginManager()

def create_app():
    app = Flask(__name__,static_url_path='/static')
    app.config.from_pyfile('settings.py')
    # app.config.from_object()
    # app.config['SECRET_KEY'] = 'the random string'
    # app.config['JWT_SECRET_KEY'] = 't1NP63m4wnBg6nyHYKfmc2TpCOGI4nss'
    # app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:maloo@localhost:5432/flask_user"
    # app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = 'mamtamaloo10@gmail.com'
    # app.config['MAIL_PASSWORD'] = 'dtrcvzldgydcjega'    # app password : https://myaccount.google.com/apppasswords
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    # app.config['MAIL_DEFAULT_SENDER'] = 'mamtamaloo10@gmail.com'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    # app.wsgi_app = Middleware(app.wsgi_app)
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager.init_app(app)
    # login_manager.login_view = "/"l

    from product.models.product_model import Product
    from order.views import order_bp
    app.register_blueprint(order_bp)

    from user.routes.user_bp import user_bp
    app.register_blueprint(user_bp)

    from product.controller.inventory_controller import inventory_bp
    app.register_blueprint(inventory_bp)

    from product.controller.product_controller import ProductControl
    app.add_url_rule("/product/", view_func=ProductControl.as_view("product_api"))
    app.add_url_rule("/product/<uuid:id>",view_func=ProductControl.as_view("product_put_api"))

    return app



