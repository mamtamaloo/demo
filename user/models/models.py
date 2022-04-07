import re
from flask_admin.contrib.sqla import ModelView
from user import db
from flask_security import UserMixin
from werkzeug.security import check_password_hash,generate_password_hash
from sqlalchemy.orm import validates
from sqlalchemy.dialects.postgresql import UUID
import uuid

class UserModel(db.Model,UserMixin):
    __tablename__ = 'user'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(),nullable=False)
    name = db.Column(db.String())
    email = db.Column(db.String(120),nullable=False)
    password = db.Column(db.String(128))
    role = db.Column(db.String(20),default="customer")
    image = db.Column(db.String(100),nullable=True)
    mobile_no = db.Column(db.String(12),nullable=False)
    #product = db.relationship('Product', backref='user', lazy=True)

    def check_password(self,password):
        return check_password_hash(self.password,password)

    def set_password(self,password):
        if not password:
            raise AssertionError('Password not provided')
        if not re.match('\d.*[A-Z]|[A-Z].*\d', password):
            raise AssertionError('Password must contain 1 capital letter and 1 number')
        if len(password) < 8:
            raise AssertionError('Password must be greater than 8 ')


    @validates('username')
    def validate_username(self, key, username):
        if not username:
            raise AssertionError('No username provided')
        if UserModel.query.filter(UserModel.username == username).first():
            raise AssertionError('Username is already in use')
        if len(username) < 5 or len(username) > 20:
            raise AssertionError('Username must be between 5 and 20 characters')
        return username

    @validates('email')
    def validate_email(self, key, email):
        if not email:
            raise AssertionError('No email provided')
        if not re.match("[^@]+@[^@]+\.[^@]+", email):
            raise AssertionError('Provided email is not an email address')
        return email


    @validates('mobile_no')
    def validate_mobile(self,key,mobile_no):
        if not mobile_no:
            raise AssertionError('No mobile number')
        if not re.match("\d+$",mobile_no):
            raise AssertionError('Mobile Number must be integer ')
        return mobile_no

