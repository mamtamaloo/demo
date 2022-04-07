import json

from flask import request, jsonify, Blueprint
from flask.views import MethodView
from flask_jwt_extended import jwt_required

from product.models.product_model import Product, Inventory
from user import db
from user.decorators import token_validate, permission_validate

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory/<product_id>', methods=['POST'])
@jwt_required()
@token_validate
@permission_validate(role="supplier")
def create(current_user,product_id):
    res = json.loads(request.data)
    stock = res['stock']
    user_id = current_user.id
    product = Product.query.filter_by(id=product_id).first()
    if not product:
        raise FileNotFoundError
    inventory = Inventory(product=product.id,stock=stock)
    inventory.save(current_user)
    db.session.add(inventory)
    db.session.commit()
    return {"message": "order has been created successfully.",
            "inventory": {
                "product": product.id,
                "stock":stock,
            }}
