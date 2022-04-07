import json
import datetime
import os

from flask_jwt_extended import create_access_token, jwt_required,decode_token
from flask import request, jsonify, Blueprint, render_template, url_for
from werkzeug.security import generate_password_hash
from user import db
from user.decorators import token_validate, permission_validate
from user.models.models import UserModel
from mail_service import send_email
from user import login_manager


@login_manager.user_loader
def load_user(user_id):
    return UserModel.get(user_id)


def hello_world():
    return 'Hello World'


def user_info():
    response = json.loads(request.data)
    # name = {'name' : request.json['name']}
    #
    # return jsonify({'name':name})

    return jsonify({'name': response['name']})


def create_user():
    res = json.loads(request.data)
    name = res['name']
    email = res['email']
    password = res['password']
    username = res['username']
    mobile_no = res['mobile_no']
    role = res['role']
    pwd_hash = generate_password_hash(password)
    user = UserModel(name=name, email=email, password=pwd_hash, username=username, mobile_no=mobile_no,role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return {"message": "user has been created successfully.",
            "user": {
                "email": email,
                "name": name,
                "username": username,
                "mobile_no": mobile_no,
            }}

def sign_in():
    res = json.loads(request.data)
    email = res['email']
    password = res['password']
    user = UserModel.query.filter_by(email=email).first()
    authorize = user.check_password(password)
    # login_user(user)
    if not authorize:
        return ({"error": "email or password is wrong"
                 })
    expires = datetime.timedelta(days=7)
    access_token = create_access_token(identity=user.id, expires_delta=expires)
    print(access_token)
    decode = decode_token(access_token)
    print(decode)

    return ({"token": access_token
             })


@jwt_required()
def list():
    name_list = []
    users = UserModel.query.all()

    for user in users:
        name_list.append(user.name)

    return jsonify(name_list)

@jwt_required()
@token_validate
@permission_validate(role=["customer","supplier"])
def update(current_user):
    data = json.loads(request.data)
    user = UserModel.query.filter_by(id=current_user.id).first()
    user.mobile_no = data['mobile_no']
    user.role = data['role']
    db.session.commit()
    return {"message": "Mobile Number has updated successfully"}

@jwt_required()
@token_validate
@permission_validate(role=["customer"])
def change_password(current_user):
    data = json.loads(request.data)
    old_password = data['old_password']
    new_password = data['new_password']
    if current_user.check_password(old_password):
        pwd_hash = generate_password_hash(new_password)
        current_user.set_password(new_password)
        current_user.password = pwd_hash
        db.session.commit()
        return {"msg":"password change successfully"}
    else:
        return {"msg":"password mismatch"}

def forgot_password():
    data = json.loads(request.data)
    url = request.host_url+'reset/'
    expires = datetime.timedelta(hours=24)
    email = data['email']
    user = UserModel.query.filter_by(email=email).first()
    reset_token = create_access_token(identity=user.id, expires_delta=expires)
    html_body = render_template('reset_password.html',
                                url=url + reset_token),
    return send_email('reset password','mamtamaloo10@gmail.com',recipients="mamtamaloo10@gmail.com",text_body="",html_body=html_body)

def reset_password():
    res = json.loads(request.data)
    reset_token = res['reset_token']
    # reset_token = reset_token
    password = res['password']
    print(decode_token(reset_token))
    user_id = decode_token(reset_token)['sub']
    user = UserModel.query.filter_by(id=user_id).first()
    pwd_hash = generate_password_hash(password)
    user.password = pwd_hash
    db.session.commit()
    return send_email("password reset successfully",sender='mamtamaloo10@gmail.com',recipients=user.email,html_body="",text_body="")
    # return {'msg':'password reset successfully'}

@jwt_required()
@token_validate
@permission_validate(role=["customer"])
def upload_file(current_user):
    from run import app
    f = request.files['file']
    path = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
    f.save(path)
    current_user.image = url_for('static',filename='upload/'+f.filename)
    db.session.commit()
    return "file upload securely"
