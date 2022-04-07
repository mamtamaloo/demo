import json
from flask import request, Blueprint, jsonify

from fundamental import OrderStatus
from product.models.product_model import Product, Inventory
from user import db
from user.decorators import token_validate, permission_validate
from order.models import Order
from flask_jwt_extended import jwt_required, exceptions
from flask_security import changeable

order_bp = Blueprint('order', __name__)


@order_bp.route('/create/<product_id>', methods=['POST'])
@jwt_required()
@token_validate
@permission_validate(role="customer")
def create_order(current_user,product_id):
    res = json.loads(request.data)
    name = res['name']
    qty = res['qty']
    user_id = current_user.id
    product = Product.query.filter_by(id=product_id).first()

    if not product:
        raise FileNotFoundError
    order = Order(name=name, user_id=user_id,qty=qty,product=product_id,price=product.price,status=OrderStatus.PLACED)
    order.save(current_user)
    db.session.add(order)
    db.session.commit()
    return {"message": "order has been created successfully.",
            "order": {
                "name": name,
                "user_id": user_id,
            }}


@order_bp.route('/order/list', methods=['GET'])
@jwt_required()
@token_validate
@permission_validate(role="customer")
def list_order(current_user):
    orders = Order.query.filter_by(user_id=current_user.id).all()
    result = []
    for order in orders:
        order_data = { }
        order_data['id'] = order.id
        order_data['name'] = order.name
        result.append(order_data)

    return jsonify({'list_of_orders': result})

@order_bp.route('/order/<order_id>', methods=['GET'])
@jwt_required()
@token_validate
@permission_validate(role="customer")
def get_order(self,current_user,order_id):
    order = Order.query.filter_by(id=order_id,user_id=current_user.id).first()
    if order:
        return {
            "order":{
                'id':order.id,
                'name':order.name
            }
        }

    else:
        return {
            "message":"Access Denied"
        }


def _validate_cancel_order(order:Order):
    if order.status in [OrderStatus.DELIVERED,OrderStatus.CANCELED]:
        raise exceptions.ValidationError("order can't cancelled")

@order_bp.route('/order/cancel/<order_id>', methods=['GET'])
@jwt_required()
@token_validate
@permission_validate(role="customer")
def cancel(current_user,order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    _validate_cancel_order(order)
    inventory = Inventory.query.filter_by(product=order.product).first()
    # if order.status in [OrderStatus.DELIVERED, OrderStatus.CANCELED]
    #     raise exceptions.ValidationError("order can't cancelled")
    # # if order.status == "DELIVERED" or order.status == "CANCELED":
    #     raise exceptions.ValidationError("order can't cancelled")
    # elif order.status != "PLACED":
    #     inventory.stock = inventory.stock + order.qty
    #     inventory.save(current_user)


    if order.status is not OrderStatus.PLACED:
        inventory.stock = inventory.stock + order.qty
        inventory.save(current_user)

    order.status = "CANCELED"
    db.session.commit()

    if order:
        return {
            "order": {
                'id': order.id,
                'name': order.name,
                #'status' : order.status
            }
        }

    else:
        return {
            "message": "Access Denied"
        }




@order_bp.route('/order/return/<order_id>', methods=['GET'])
@jwt_required()
@token_validate
@permission_validate(role="customer")
def return_order(self,current_user,order_id):
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    order.status = "RETURNED"
    db.session.commit()

    if order:
        return {
            "order": {
                'id': order.id,
                'name': order.name,
                'status': order.status
            }
        }

    else:
        return {
            "message": "Access Denied"
        }


def check_inventory_available(order):
    inventory = Inventory.query.filter_by(product=order.product).first()
    if not inventory:
        raise exceptions.APIException("inventory not found")
    if order.qty > inventory.stock:
        raise exceptions.ValidationError("out of stock")

def _update_stock(product:Product, qty:int,current_user):
    inventory = Inventory.query.filter_by(product=product).first()
    if not inventory:
        raise AttributeError("None Type Object")

    inventory.stock = inventory.stock - qty
    if inventory.stock <= 0:
        inventory.status = "out of stock"
    inventory.save(current_user)
    db.session.commit()

@order_bp.route('/order/accept/<order_id>', methods=['GET'])
@jwt_required()
@token_validate
@permission_validate(role="supplier")
def accept(current_user,order_id):
    order = Order.query.filter_by(id=order_id).first()
    check_inventory_available(order)
    if order.status == OrderStatus.PLACED:
        order.status = OrderStatus.PROCEED
        qty = order.qty
        #order.supplier = supplier
        _update_stock(order.product, qty,current_user)
        # else:
        #     order.status = OrderStatus.REJECTED

    # elif order.status == OrderStatus.PENDING:
    #     if order.reason in [ReturnReason.PACKAGING, ReturnReason.INFERIORITY]:
    #         order.status = OrderStatus.RETURNED
    #         qty = order.qty
    #         order.supplier = supplier
    #         SspOrderUseCase._update_stock(order.product, qty, order.type)
    #     else:
    #         order.status = OrderStatus.REJECTED
    else:
        raise ValueError('Invalid access******.')
    order.save(current_user)

    db.session.commit()

    if order:
        return {
            "order": {
                'id': order.id,
                'name': order.name,
                #'status': order.status
            }
        }

    else:
        return {
            "message": "Access Denied"
        }

