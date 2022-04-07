from flask_admin.contrib.sqla import ModelView
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from user import create_app,db
from flask_mail import Mail
from flask_admin import Admin

from user.models.models import UserModel

app = create_app()
jwt = JWTManager(app)
mail = Mail(app)
admin = Admin(app)

admin.add_view(ModelView(UserModel,db.session))

if __name__ == '__main__':
    app.run()
