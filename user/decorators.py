from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from user.models.models import UserModel


def token_validate(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        user_id = get_jwt_identity()
        try:
            current_user = UserModel.query.filter_by(id=user_id).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(*args, **kwargs)

    return decorator


def permission_validate(role=None):
    def check_permission(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = None
            user_id = get_jwt_identity()
            current_user = UserModel.query.filter_by(id=user_id).first()
            if current_user.role in role:
                return f(current_user,*args, **kwargs)
            else:
                raise PermissionError

        return decorator
    return check_permission
