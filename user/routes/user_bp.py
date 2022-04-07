from flask import Blueprint
from user.controller.user_controller import user_info, create_user, sign_in, list, update,change_password,forgot_password,reset_password,upload_file
user_bp = Blueprint('user_bp',__name__)

user_bp.route('/user_info', methods=['POST'])(user_info)
user_bp.route('/register', methods=['POST'])(create_user)
user_bp.route('/signin', methods=['POST'])(sign_in)
user_bp.route('/list', methods=['GET'])(list)
user_bp.route('/update', methods=['PUT'])(update)
user_bp.route('/change_password', methods=['PUT'])(change_password)
user_bp.route('/forgot_password', methods=['GET'])(forgot_password)
user_bp.route('/reset', methods=['POST'])(reset_password)
user_bp.route('/image', methods=['POST'])(upload_file)
